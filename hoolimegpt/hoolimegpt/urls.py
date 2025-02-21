"""
URL configuration for hoolimegpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from home.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', about, name='home'),
    path('', pending, name='pending'),
    path('edit/<int:id>/', home, name='edit_oasis_info'),

    path('about/', about, name='about'),

    path('pending/', pending, name='pending'),
    path('pending/', pending_oasis_forms, name='pending_oasis_forms'),

    path('complete/', complete, name='complete'),
    path("admin/", admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('logout/', logout_view, name='logout'),

    path('img_view/', about, name='img_view.html'),

    path('home/<int:id>/', home, name='home'),
    path('home/', home, name='home'),
    path('remove_image/', remove_image, name='remove_image'),


    path('capture-and-edit/', capture_and_edit, name='capture_and_edit'),

    path("extract/", extract, name="ocr_extract"),

    # path("transcription/", transcription_view, name="transcription")


    # path('send-otp/', send_otp, name='send_otp'),
    # path('verify-otp/', verify_otp, name='verify_otp'),
    # path('reset-password/', reset_password, name='reset_password'),
    # path('update-password/', update_password, name='update_password'),

    # path('send-reset-link/', send_reset_link, name='send_reset_link'),








] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
