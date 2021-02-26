from django.contrib import admin
from .models import ReferralCode, Referral, Wallet

admin.site.register(ReferralCode, Referral, Wallet)
