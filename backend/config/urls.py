from django.urls import path
from django.conf import settings
from apps.profilr.views import filter, login, root, incident_index, incident_detail, image_full, image_thumbnail


urlpatterns = [
    path("", root, name="root"),
    path("filter/", filter, name="filter"),
    path("login/", login, name="login"),
    path("incident/", incident_index, name="incident_index"),
    path("incident/<int:id>", incident_detail, name="incident_detail"),
    path("image/<int:id>", image_full, name="image_full"),
    path("image/<int:id>/thumbnail", image_thumbnail, name="image_thumbnail"),
]
