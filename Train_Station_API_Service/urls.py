"""
URL configuration for Train_Station_API_Service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls.conf import include
from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import UserViewSet

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from Train_Station_API_Service import settings


urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("train-station-ap1/", include("station.urls"), name="train-station-ap1"),
                  path("user/", include("user.urls"), name="user"),
                  path("api/doc/schema/", SpectacularAPIView.as_view(), name="schema"),
                  path(
                      "api/doc/swagger/",
                      SpectacularSwaggerView.as_view(url_name="schema"),
                      name="swagger-ui",
                  ),
                  path(
                      "api/doc/redoc/",
                      SpectacularRedocView.as_view(url_name="schema"),

                      name="redoc",
                  ),
                  path("__debug__/", include("debug_toolbar.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)