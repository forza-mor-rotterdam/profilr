from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = "apps.services"
    verbose_name = "Services"

    def ready(self) -> None:

        return super().ready()
