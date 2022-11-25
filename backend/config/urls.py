from apps.profilr.views import (
    filter,
    image_full,
    image_thumbnail,
    incident_detail,
    incident_index,
    login,
    logout,
    root,
)
from django.urls import path
from django.conf import settings
from apps.profilr.views import filter, login, logout, root, incident_index, incident_detail, image_full, image_thumbnail
from django.urls import include, path


urlpatterns = [
    path("", root, name="root"),
    path("filter/", filter, name="filter"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("incident/", incident_index, name="incident_index"),
    path("incident/<int:id>", incident_detail, name="incident_detail"),
    path("image/<int:id>", image_full, name="image_full"),
    path("image/<int:id>/thumbnail", image_thumbnail, name="image_thumbnail"),

    path("health/", include('health_check.urls')),
]
