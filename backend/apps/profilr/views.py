import copy

from apps.auth.backends import authenticate
from apps.auth.decorators import login_required
from apps.profilr.forms import HANDLE_OPTIONS, HandleForm
from apps.services import msb_api_service
from apps.services.msb import VALID_FILTERS
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
    profile = request.user.profile
    user_token = request.user.token
    if request.POST:
        profile = {
            "filters": {f: request.POST.getlist(f, []) for f in VALID_FILTERS},
        }
        profile = request.user.set_profile(profile)

    valid_filters = msb_api_service.validate_filters(profile.get("filters"))
    filters = copy.deepcopy(valid_filters)

    departments = msb_api_service.get_afdelingen(user_token)
    msb_api_service.get_onderwerpgroepen(user_token)
    areas = msb_api_service.get_wijken(user_token)

    # create lookups for filter options
    afdelingen_dict = {d.get("code"): d.get("omschrijving") for d in departments}
    wijken_dict = {w.get("code"): w.get("omschrijving") for w in areas}
    buurten_dict = {
        b.get("code"): b.get("omschrijving")
        for w in areas
        for b in w.get("buurten", [])
    }
    # add readable filter results like: [[id, name]]
    filters["wijken"] = [[o, wijken_dict.get(o, o)] for o in filters.get("wijken", [])]
    filters["buurten"] = [
        [o, buurten_dict.get(o, o)] for o in filters.get("buurten", [])
    ]
    filters["afdelingen"] = [
        [o, afdelingen_dict.get(o, o)] for o in filters.get("afdelingen", [])
    ]
    filters_count = len([vv for k, v in filters.items() for vv in v])
    incident_count = 0
    if filters_count > 0:
        incidents = msb_api_service.get_list(
            user_token, data=valid_filters, no_cache=True
        )
        incident_count = len(incidents)
    return render(
        request,
        "filters/form.html",
        {
            "filters": filters,
            "valid_filters": valid_filters,
            "areas": areas,
            "profile": profile,
            "departments": departments,
            "filters_count": filters_count,
            "incident_count": incident_count,
            "active_filter_open": request.POST.get("active_filter_open", "false"),
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

        incidents = [
            {
                **incidents[i],
                **{
                    "detail": msb_api_service.get_detail(
                        incidents[i].get("id"), user_token
                    )
                    if i < PAGE_SIZE
                    else {}
                },
            }
            for i in range(len(incidents))
        ]

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
    areas = msb_api_service.get_wijken(user_token)

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
def incident_handle(request, id=None):
    profile = request.user.profile
    user_token = request.user.token
    incident = msb_api_service.get_detail(id, user_token)

    form = HandleForm()
    warnings = None
    errors = None
    messages = None

    if request.POST:
        print(request.POST)
        form = HandleForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get("handle_choice", 1)
            choice_type = {
                x: HANDLE_OPTIONS[x][0] for x in range(len(HANDLE_OPTIONS))
            }.get(int(choice), choice)
            choice_value = {
                x: HANDLE_OPTIONS[x][1] for x in range(len(HANDLE_OPTIONS))
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

    return render(
        request,
        "incident/handle.html",
        {
            "id": id,
            "incident": incident,
            "profile": profile,
            "form": form,
            "errors": errors,
            "warnings": warnings,
            "messages": messages,
        },
    )


@login_required
def image_thumbnail(request, id):
    return image_full(request, id, True)


@login_required
def image_full(request, id, thumbnail=False):
    blob = msb_api_service.get_foto(id, request.user.token, thumbnail)
    return FileResponse(blob)
