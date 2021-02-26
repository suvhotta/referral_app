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
