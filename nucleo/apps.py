from django.apps import AppConfig


class NucleoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nucleo'
    verbose_name = 'Núcleo Institucional e Configurações'

    def ready(self):
        # Registra verificações customizadas de sistema para SEO e Segurança
        import nucleo.checks  # noqa: F401

        # Aplica proteção contra brute force na view de login do Django Admin
        from django.contrib import admin
        from nucleo.rate_limit import wrap_admin_login
        wrap_admin_login(admin.site)
