from rest_framework import status
from rest_framework.response import Response
from referral.serializers import (
    UserSerializer, 
    UserLoginSerializer, 
    WalletSerializer,
    ReferralCodeSerializer
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from referral.models import Wallet, ReferralCode

class RegisterView(views.APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key}, status=201)


class WalletDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return JsonResponse(serializer.data, status=200)


class ReferralView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = ReferralCode.objects.get(user=request.user)
        serializer = ReferralCodeSerializer(code)
        return JsonResponse(serializer.data, status=200)
    
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ReferralCodeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": f"Referral code sent to {serializer.validated_data.get('to_email')}"}, status=202)
        return JsonResponse(serializer.errors, status=400)