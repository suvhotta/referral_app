"""referral_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import referral.views as referral_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', referral_views.RegisterView.as_view(), name='register'),
    path('login/', referral_views.UserLoginView.as_view(), name='login'),
    path('wallet/', referral_views.WalletDetailView.as_view(), name='wallet-details'),
    path('referral/', referral_views.ReferralView.as_view(), name='referral'),
]
