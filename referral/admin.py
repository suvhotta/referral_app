from django.contrib import admin
from .models import ReferralCode, Referral, Wallet

models = [ReferralCode, Referral, Wallet]
admin.site.register(models)
