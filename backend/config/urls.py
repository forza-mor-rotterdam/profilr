from apps.profilr.views import (
    filter,
    http_404,
    http_500,
    image_full,
    image_thumbnail,
    incident_detail,
    incident_index,
    incident_list,
    incident_list_item,
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
    path("part/filter/", filter, name="filter_part"),
    path("part/incident-list/", incident_list, name="incident_list_part"),
    path(
        "part/incident-list-item//<int:id>",
        incident_list_item,
        name="incident_list_item_part",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
