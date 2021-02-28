from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from referral.models import Referral, ReferralCode, Wallet
from referral.services import CreateReferral, SendReferral
from rest_framework.validators import ValidationError


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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username',"")
        password = data.get('password',"")
        if username and password:
            user = authenticate(**data)
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    raise ValidationError("Your account has been suspended", code=404)
            else:
                raise ValidationError("Please check your credentials and try again!", code=401)
        else:
            raise ValidationError("Please enter both username and password to login!", code=401)
        return data


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['credits']


class ReferralCodeSerializer(serializers.ModelSerializer):
    to_email = serializers.EmailField(write_only=True)

    class Meta:
        model = ReferralCode
        fields = ['code', 'to_email']
        extra_kwargs = {'code':{'read_only':True}}

    def create(self, validated_data):
        to_email = validated_data.get('to_email')
        current_user =  self.context['request'].user
        code = ReferralCode.objects.get(user=current_user).code
        sendReferral = SendReferral(mail_id=to_email, referral_code=code)
        sendReferral.send_referral_mail()
        return validated_data