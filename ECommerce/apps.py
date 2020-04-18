from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    name = 'ECommerce'

    def ready(self):
        import ECommerce.signals