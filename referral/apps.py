from django.apps import AppConfig


class ReferralConfig(AppConfig):
    name = 'referral'

    def ready(self):
        import referral.signals
