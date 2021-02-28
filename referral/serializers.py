from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from referral.models import Referral, ReferralCode, Wallet
from referral.services import CreateReferral


class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(max_length=154, write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'referral_code']
        extra_kwargs = {'password':{'write_only':True}}
   
    def create(self, validated_data):
        """
        Creates a new user with/without referral code.
        """
        referral_code = ''
        referred_by = ''
        if validated_data.get('referral_code'):
            referral_code = validated_data.pop('referral_code')
            try:
                referred_by = ReferralCode.objects.get(code=referral_code).user
            except ObjectDoesNotExist:
                pass
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        if referred_by:
            referral = CreateReferral(referred_by=referred_by, referred_to=user)
            referral.new_referral()
            for value in (referred_by, user):
                wallet = Wallet.objects.get(user=value)
                wallet.credits += 100
                wallet.save()
        return user
