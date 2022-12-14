import copy
from collections import Counter

from apps.auth.backends import authenticate
from apps.auth.decorators import login_required
from apps.profilr.forms import HANDLED_OPTIONS, HandleForm
from apps.profilr.utils import get_filter_options
from apps.services import msb_api_service
from apps.services.msb import VALID_FILTERS
from django.conf import settings
from django.core.cache import cache
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

PAGE_SIZE = 10


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


def http_response(request):
    return HttpResponse("<h1>Hello HttpResponse</h1>")


def root(request):
    if request.user and request.user.is_authenticated:
        return redirect(reverse("incident_index"))
    return redirect(reverse("login"))


def logout(request):
    msb_api_service.logout()
    request.session.flush()
    return redirect(reverse("root"))


def login(request):
    if request.user and request.user.is_authenticated:
        return redirect(reverse("incident_index"))

    error = None
    if request.POST:
        success, result = authenticate(
            request=request,
            username=request.POST.get("_username"),
            password=request.POST.get("_password"),
        )
        print(result)
        if success:
            return redirect(reverse("incident_index"))
        else:
            error = result
    print("render")
    return render(
        request,
        "login/index.html",
        {
            "last_username": request.POST.get("_username", ""),
            "error": error,
        },
    )


@login_required
def filter(request):
    FILTERS = "filters"
    AFDELINGEN = "afdelingen"
    profile = request.user.profile
    user_token = request.user.token
    if request.POST:
        profile = {
            FILTERS: {f: request.POST.getlist(f, []) for f in VALID_FILTERS},
        }
        if not profile[FILTERS][AFDELINGEN]:
            profile = {
                FILTERS: {f: [] for f in VALID_FILTERS},
            }
        profile = request.user.set_profile(profile)

    valid_filters = msb_api_service.validate_filters(profile.get(FILTERS))

    filters = copy.deepcopy(valid_filters)

    filters, departments, categories, areas = get_filter_options(filters, user_token)

    filters_count = len([vv for k, v in filters.items() for vv in v])
    incident_count = 0
    if filters_count > 0:
        incidents = msb_api_service.get_list(
            user_token, data=valid_filters, no_cache=True
        )
        incident_count = len(incidents)

        # START: Experimental: Calculate melding count for each filter
        found_afdelingen = Counter([i.get("afdeling", {}).get("id") for i in incidents])
        # found_onderwerpen = Counter(
        #     [i.get("onderwerp", {}).get("id") for i in incidents]
        # )

        filters[AFDELINGEN] = [
            [o[0], o[1], found_afdelingen.get(o[0])]
            for o in filters.get(AFDELINGEN, [])
        ]
        departments = [
            {
                **d,
                "meldingen_count": found_afdelingen.get(d.get("code"), 0),
            }
            for d in departments
        ]
        # END: Experimental: Calculate melding count for each filter
    return render(
        request,
        "filters/form.html",
        {
            FILTERS: filters,
            "valid_filters": valid_filters,
            "profile": profile,
            "areas": areas,
            "departments": departments,
            "categories": categories,
            "filters_count": filters_count,
            "incident_count": incident_count,
            "foldout_states": request.POST.get("foldout_states", []),
        },
    )


@login_required
def incident_list(request):
    profile = request.user.profile
    user_token = request.user.token
    valid_filters = msb_api_service.validate_filters(profile.get("filters"))

    filters_count = len([vv for k, v in valid_filters.items() for vv in v])

    # get incidents if we have filters
    incidents = []
    if filters_count > 0:
        incidents = msb_api_service.get_list(
            user_token, data=valid_filters, no_cache=True
        )

        # temp: spoed key only available in list items, set cache for it
        for i in incidents:
            cache_key = f"incident_{i.get('id')}_spoed"
            cache.set(cache_key, bool(i.get("spoed")), 60 * 60 * 24)

    return render(
        request,
        "incident/list.html",
        {
            "incidents": incidents,
            "filters_count": filters_count,
            "filters": valid_filters,
        },
    )


@login_required
def incident_index(request):
    return render(
        request,
        "incident/index.html",
        {
            "main_view": reverse("incident_list_part"),
            "fullpage_view": reverse("filter_part"),
        },
    )


@login_required
def incident_detail(request, id):
    profile = request.user.profile
    user_token = request.user.token

    incident = msb_api_service.get_detail(id, user_token)
    categories = msb_api_service.get_onderwerpgroepen(user_token)
    sub_cat_ids = {
        sub_cat.get("id"): cat
        for cat in categories
        for sub_cat in cat.get("onderwerpen")
    }
    incident["groep"] = sub_cat_ids.get(incident.get("onderwerp", {}).get("id"))
    spoed_cache_key = f"incident_{incident.get('id')}_spoed"
    areas = msb_api_service.get_wijken(user_token)

    incident = {
        **incident,
        **{
            "spoed": cache.get(spoed_cache_key, False),
        },
    }

    return render(
        request,
        "incident/detail.html",
        {
            "id": id,
            "incident": incident,
            "groupedSubjects": categories,
            "areas": areas,
            "profile": profile,
        },
    )


@login_required
def incident_list_item(request, id):
    user_token = request.user.token
    incident = msb_api_service.get_detail(id, user_token)
    spoed_cache_key = f"incident_{incident.get('id')}_spoed"
    incident = {
        **incident,
        **{
            "spoed": cache.get(spoed_cache_key, False),
        },
    }

    return render(
        request,
        "incident/list_item.html",
        {
            "incident": incident,
        },
    )


@login_required
def incident_modal_handle(request, id, handled_type=None):
    if not handled_type:
        return HttpResponse("")
    user_token = request.user.token
    incident = msb_api_service.get_detail(id, user_token)
    form = HandleForm(handled_type=handled_type)
    warnings = []
    errors = []
    messages = []
    form_submitted = False
    is_handled = False

    if request.POST:
        form = HandleForm(request.POST, handled_type=handled_type)
        if form.is_valid():
            choice = form.cleaned_data.get("handle_choice", 1)
            choice_type = {
                x: HANDLED_OPTIONS[x][0] for x in range(len(HANDLED_OPTIONS))
            }.get(int(choice), choice)
            choice_value = {
                x: HANDLED_OPTIONS[x][1] for x in range(len(HANDLED_OPTIONS))
            }.get(int(choice), choice)
            data = {
                "meldingId": incident.get("id"),
                "behandelaar": request.user.name,
                "meldingType": choice_type,
                "afhandelOpmerking": choice_value,
                "straat": incident.get("locatie", {})
                .get("adres", {})
                .get("straatNummer"),
                "huisnummer": incident.get("locatie", {})
                .get("adres", {})
                .get("huisnummer"),
                "plaatsbepaling": incident.get("locatie", {}).get("plaatsbepaling", 0),
                "x": incident.get("locatie", {}).get("x", 0),
                "y": incident.get("locatie", {}).get("y", 0),
            }
            print(data)
            result = msb_api_service.afhandelen(incident.get("id"), user_token, data)
            print(result)
            if result.get("warnings"):
                warnings = result.get("warnings")
            if result.get("errors"):
                errors = result.get("errors")
            if result.get("messages"):
                messages = result.get("messages")
            form = None
            form_submitted = True
            is_handled = not warnings and not errors
            if not settings.ENABLE_MELDING_AFHANDELEN:
                messages.append(
                    "In deze omgeving kunnen meldingen niet worden afgehanded!"
                )

    return render(
        request,
        "incident/modal_handle.html",
        {
            "incident": incident,
            "handled_type": handled_type,
            "form": form,
            "form_submitted": form_submitted,
            "HANDLED_OPTIONS": HANDLED_OPTIONS,
            "parent_context": {
                "form_submitted": form_submitted,
                "errors": errors,
                "warnings": warnings,
                "messages": messages,
                "is_handled": is_handled,
            },
        },
    )


@login_required
def image_thumbnail(request, id):
    return image_full(request, id, True)


@login_required
def image_full(request, id, thumbnail=False):
    blob = msb_api_service.get_foto(id, request.user.token, thumbnail)
    return FileResponse(blob)


def config(request):
    return render(
        request,
        "config.html",
    )
