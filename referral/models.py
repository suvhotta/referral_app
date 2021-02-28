from django.db import models
from django.contrib.auth.models import User
import secrets

class ReferralCode(models.Model):
    """
    Model for referral code.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=154, unique=True)

    def generate_code(self):
        username = self.user.username
        random_code = secrets.token_hex(2)
        return username+random_code

    def save(self, *args, **kwargs):
        self.code = self.generate_code()

        return super(ReferralCode, self).save(*args, **kwargs)


class Referral(models.Model):
    """
    For capturing who referred whom.
    """
    referred_by = models.ForeignKey(User, unique=False, on_delete=models.DO_NOTHING, related_query_name='my_referral')
    referred_to = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_query_name='has_referred')


class Wallet(models.Model):
    """
    Wallet to store User's credits.
    """
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    credits = models.FloatField(default=0.0)