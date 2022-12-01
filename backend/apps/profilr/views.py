from apps.services import msb_api_service, profilr_api_service
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

DEFAULT_FILTERS = {"radius": 200, "x": 92441, "y": 437718}
DEFAULT_PROFILE = {"filters": DEFAULT_FILTERS}
PAGE_SIZE = 10


def get_profile(request) -> tuple[tuple[bool, dict], tuple[bool, str]]:
    if request.session.get("is_logged_in", False):
        user_token = request.session.get("msb_token", False)
        if user_token:
            try:
                if settings.ENABLE_PROFILR_API:
                    profile = profilr_api_service.get_profile(user_token)
                else:
                    profile = msb_api_service.get_user_info(user_token)
                    profile = request.session.get("profile", DEFAULT_PROFILE)
                if not profile.get("filters"):
                    profile["filters"] = DEFAULT_FILTERS
                return profile, user_token
            except Exception:
                pass

    msb_api_service.logout()
    request.session["msb_token"] = None
    request.session["profile"] = DEFAULT_PROFILE
    request.session["is_logged_in"] = False
    return False, False


def set_profile(profile: dict, user_token: str, request) -> dict:
    if settings.ENABLE_PROFILR_API:
        profile = profilr_api_service.set_profile(user_token, profile)
    else:
        request.session["profile"] = profile
    return profile


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
    if not request.session.get("is_logged_in", False):
        return redirect(reverse("login"))

    return redirect(reverse("incident_index"))


def logout(request):
    msb_api_service.logout()
    request.session["msb_token"] = None
    request.session["profile"] = DEFAULT_PROFILE
    request.session["is_logged_in"] = False
    return redirect(reverse("root"))


def login(request):
    if request.session.get("is_logged_in"):
        return redirect(reverse("incident_index"))

    error = None
    if request.POST:
        success, user_token = msb_api_service.login(
            request.POST.get("_username"),
            request.POST.get("_password"),
        )
        if success:
            request.session["msb_token"] = user_token
            request.session["is_logged_in"] = True

            return redirect(reverse("incident_index"))
        else:
            request.session["is_logged_in"] = False
            error = "invalid_username_or_password"

    return render(
        request,
        "login/index.html",
        {
            "last_username": request.POST.get("_username", ""),
            "error": error,
        },
    )


def filter(request):
    profile, user_token = get_profile(request)
    if not user_token:
        return redirect(reverse("login"))

    areas = msb_api_service.get_wijken(user_token)
    departments = msb_api_service.get_afdelingen(user_token)
    categories = msb_api_service.get_onderwerpgroepen(user_token)

    print(request.POST)
    if request.POST:
        data = {
            "filters": {
                "wijken": request.POST.getlist("wijken"),
                "buurten": request.POST.getlist("buurten"),
                "afdelingen": request.POST.getlist("afdelingen"),
            }
        }
        set_profile(data, user_token, request)
        return redirect(reverse("incident_index"))

    return render(
        request,
        "filter/index.html",
        {
            "areas": areas,
            "departments": departments,
            "categories": categories,
        },
    )


def incident_index(request):
    profile, user_token = get_profile(request)
    if not user_token:
        return redirect(reverse("login"))

    print(profile)
    print(request.POST)
    if request.POST:
        filter_options = ("wijken", "buurten", "afdelingen", "groepen", "onderwerpen")
        profile = {
            "filters": {f: request.POST.getlist(f, []) for f in filter_options},
        }
        profile = set_profile(profile, user_token, request)

    # clean filters
    profile["filters"] = {
        k: v if type(v) == list else [v] if type(v) in [str, int, float] else []
        for k, v in profile.get("filters", {}).items()
    }
    print(profile)
    filters = profile.get("filters", DEFAULT_PROFILE.get("filters"))
    incidents = msb_api_service.get_list(user_token, data=filters, no_cache=True)

    incidents = [
        {
            **incidents[i],
            **{
                "detail": msb_api_service.get_detail(incidents[i].get("id"), user_token)
                if i < PAGE_SIZE
                else {}
            },
        }
        for i in range(len(incidents))
    ]

    departments = msb_api_service.get_afdelingen(user_token)
    categories = msb_api_service.get_onderwerpgroepen(user_token)
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
    filters_coount = len([vv for k, v in filters for vv in v])

    return render(
        request,
        "incident/index.html",
        {
            "incidents": incidents,
            "groupedSubjects": categories,
            "filters": filters,
            "areas": areas,
            "profile": profile,
            "departments": departments,
            "filters_coount": filters_coount,
        },
    )


def incident_detail(request, id):
    profile, user_token = get_profile(request)
    if not user_token:
        return redirect(reverse("login"))

    user_token = request.session.get("msb_token")
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


def image_thumbnail(request, id):
    return image_full(request, id, True)


def image_full(request, id, thumbnail=False):
    if not request.session.get("is_logged_in"):
        return redirect(reverse("login"))
    user_token = request.session.get("msb_token")

    blob = msb_api_service.get_foto(id, user_token, thumbnail)
    return FileResponse(blob)
