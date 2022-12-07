from apps.profilr.views import (
    filter,
    http_404,
    http_500,
    http_response,
    image_full,
    image_thumbnail,
    incident_detail,
    incident_handle,
    incident_index,
    incident_list,
    login,
    logout,
    root,
)
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("", root, name="root"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("incident/", incident_index, name="incident_index"),
    path("incident/<int:id>", incident_detail, name="incident_detail"),
    path("image/<int:id>", image_full, name="image_full"),
    path("image/<int:id>/thumbnail", image_thumbnail, name="image_thumbnail"),
    path("health/", include("health_check.urls")),
    path("part/incident-handle", incident_handle, name="incident_handle_default"),
    path("part/incident-handle/<int:id>", incident_handle, name="incident_handle"),
    path("part/filter/", filter, name="filter_part"),
    path("part/incident-list/", incident_list, name="incident_list_part"),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
