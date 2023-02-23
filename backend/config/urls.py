from apps.profilr.views import (
    config,
    filter,
    http_404,
    http_500,
    image_full,
    image_thumbnail,
    incident_detail,
    incident_list,
    incident_list_item,
    incident_list_page,
    incident_modal_handle,
    incident_mutation_lines,
    login,
    logout,
    root,
    ui_settings_handler,
)
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("", root, name="root"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path(
        "incident/",
        incident_list_page,
        name="incident_index",
    ),
    path("incident/<int:id>/", incident_detail, name="incident_detail"),
    path(
        "incident/<int:id>/mutation-lines/",
        incident_mutation_lines,
        name="mutation_lines",
    ),
    path("image/<int:id>/", image_full, name="image_full"),
    path("image/<int:id>/thumbnail/", image_thumbnail, name="image_thumbnail"),
    path("config/", config, name="config"),
    path("health/", include("health_check.urls")),
    # START partials
    path("part/pageheader-form/", ui_settings_handler, name="pageheader_form_part"),
    path("part/filter/", filter, name="filter_part"),
    path("part/incident-list/", incident_list, name="incident_list_part"),
    path(
        "part/incident-list-item/<int:id>/",
        incident_list_item,
        name="incident_list_item_part",
    ),
    path(
        "part/incident-modal-handle/<int:id>/",
        incident_modal_handle,
        name="incident_modal_handle_part",
    ),
    path(
        "part/incident-modal-handle/<int:id>/<str:handled_type>/",
        incident_modal_handle,
        name="incident_modal_handled_type_part",
    ),
    # END partials
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
