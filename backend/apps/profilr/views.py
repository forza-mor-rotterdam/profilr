import json

from apps.services import msb_api_service, profilr_api_service
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def http_response(request):
    return HttpResponse("<h1>Hello HttpResponse</h1>")


def root(request):
    if not request.session.get("is_logged_in", False):
        return redirect(reverse("login"))

    if request.session.get("profile", None):
        return redirect(reverse("filter"))
    return redirect(reverse("incident_index"))


def logout(request):
    msb_api_service.logout()
    del request.session["msb_token"]
    request.session["is_logged_in"] = False
    return redirect(reverse("root"))


def login(request):
    request.session["session_var"] = "session_value"
    if request.session.get("is_logged_in", False):
        return redirect(reverse("filter"))
    error = None
    if request.POST:
        success, user_token = msb_api_service.login(
            request.POST.get("_username"),
            request.POST.get("_password"),
        )
        if success:
            request.session["msb_token"] = user_token
            request.session["is_logged_in"] = True

            # return redirect(reverse("filter"))
        else:
            request.session["is_logged_in"] = False
            error = "invalid_username_or_password"

    return render(
        request,
        "login/index.html",
        {
            "last_username": request.POST.get("_username", ""),
            "error": error,
            "token": request.session.get("msb_token"),
            "logged_in": request.session.get("is_logged_in"),
        },
    )


def filter(request):

    if not request.session.get("is_logged_in", False):
        return redirect(reverse("login"))

    user_token = request.session.get("msb_token")
    areas = msb_api_service.get_wijken(user_token)
    departments = msb_api_service.get_afdelingen(user_token)
    categories = msb_api_service.get_onderwerpgroepen(user_token)

    if request.POST:
        data = {
            "filters": {
                "wijken": request.POST.get("wijken"),
                "buurten": request.POST.get("buurten"),
                "afdelingen": request.POST.get("afdelingen"),
            }
        }
        if settings.ENABLE_PROFILR_API:
            profilr_api_service.set_profile(user_token, data)
        request.session["profile"] = data
        return redirect(reverse("incident_index"))

    return render(
        request,
        "filter/index.html",
        {
            "areas": json.dumps(areas),
            "departments": json.dumps(departments),
            "categories": categories,
        },
    )


def incident_index(request):
    if not request.session.get("is_logged_in", False):
        return redirect(reverse("login"))

    user_token = request.session.get("msb_token")
    profile = request.session.get("profile", {})
    if settings.ENABLE_PROFILR_API:
        profile = profilr_api_service.get_profile(user_token)
    print(profile)
    filters = profile.get("filters", {})
    incidents = msb_api_service.get_list(user_token, data=filters, no_cache=True)
    print(incidents)
    incidents = [
        {**i, **{"detail": msb_api_service.get_detail(i.get("id"), user_token)}}
        for i in incidents
    ]

    categories = msb_api_service.get_onderwerpgroepen(user_token)

    return render(
        request,
        "incident/index.html",
        {
            "incidents": incidents,
            "groupedSubjects": categories,
        },
    )


def incident_detail(request, id):
    if not request.session.get("is_logged_in"):
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
