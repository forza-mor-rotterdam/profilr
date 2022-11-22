from django.shortcuts import render, redirect
from apps.services.msb import MSBService
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import template
import json
from django.http import FileResponse


def root(request):
    if not request.session.get('is_logged_in'):
        return redirect(reverse("login"))

    wijken = request.session['wijken']
    buurten = request.session['buurten']
    afdelingen = request.session['afdelingen']

    if not wijken or not buurten or not afdelingen:
        return redirect(reverse("filter"))
    return redirect(reverse("incident_index"))
    

def login(request):
    if request.session.get('is_logged_in'):
        return redirect(reverse("filter"))
    error = None
    if request.POST:
        success, user_token = MSBService.login(
            request.POST.get("_username"),
            request.POST.get("_password"),
        )
        if success:
            request.session['msb_token'] = user_token
            request.session['is_logged_in'] = True

            return redirect(reverse("filter"))
        else:
            request.session['is_logged_in'] = False
            error = "invalid_username_or_password"


    return render(
        request,
        'login/index.html',
        {
            "last_username": request.POST.get("_username", ""),
            "error": error,
        },
    )

def filter(request):

    if not request.session.get('is_logged_in'):
        return redirect(reverse("login"))

    user_token = request.session.get('msb_token')
    areas = MSBService.get_wijken(user_token).get("result", [])
    departments = MSBService.get_afdelingen(user_token).get("result", [])
    categories = MSBService.get_onderwerpgroepen(user_token).get("result", [])

    if request.POST:
        request.session['wijken'] = request.POST.get("wijken")
        request.session['buurten'] = request.POST.get("buurten")
        request.session['afdelingen'] = request.POST.get("afdelingen")
        return redirect(reverse("incident_index"))

    return render(
        request,
        "filter/index.html",
        {
            "areas": json.dumps(areas),
            "departments": json.dumps(departments),
            "categories": categories,
        }
    )

def incident_index(request):
    if not request.session.get('is_logged_in'):
        return redirect(reverse("login"))

    user_token = request.session.get('msb_token')
    wijken = request.session.get("wijken", [])
    buurten = request.session.get("buurten", [])
    afdelingen = request.session.get("afdelingen", [])

    filters = {
        "wijken": wijken,
        "buurten": buurten,
        "afdelingen": afdelingen,
    }
    incidents = MSBService.get_list(user_token, filters, no_cache=True).get("result", [])

    incidents = [{**i, **{
        "detail": MSBService.get_detail(i.get("id"), user_token).get("result", {})
    }} for i in incidents]
    print(incidents)
    categories = MSBService.get_onderwerpgroepen(user_token).get("result", [])

    return render(
        request,
        "incident/index.html",
        {
            "incidents": incidents,
            "groupedSubjects": categories,
        }
    )

def incident_detail(request, id):
    if not request.session.get('is_logged_in'):
        return redirect(reverse("login"))

    user_token = request.session.get('msb_token')
    incident = MSBService.get_detail(id, user_token).get("result", {})
    categories = MSBService.get_onderwerpgroepen(user_token).get("result", [])
    sub_cat_ids = {sub_cat.get("id"): cat for cat in categories for sub_cat in cat.get("onderwerpen")}
    incident["groep"] = sub_cat_ids.get(incident.get("onderwerp", {}).get("id"))
    areas = MSBService.get_wijken(user_token).get("result", [])

    return render(
        request,
        "incident/detail.html",
        {
            "id": id,
            "incident": incident,
            "groupedSubjects": categories,
            "areas": areas,
        }
    )


def image_thumbnail(request, id):
    return image_full(request, id, True)


def image_full(request, id, thumbnail=False):
    if not request.session.get('is_logged_in'):
        return redirect(reverse("login"))
    user_token = request.session.get('msb_token')

    blob = MSBService.get_foto(id, user_token, thumbnail)
    return FileResponse(blob)
    