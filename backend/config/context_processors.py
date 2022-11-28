from django.conf import settings


def general_settings(context):
    return {
        "git_sha": settings.GIT_SHA,
    }
