"""
URL configuration for car_dealer project.

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
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  #  Correct Import for Login
    TokenRefreshView,  #  Correct Import for Token Refresh
)

from marketplace.views.auth_views import RegisterView


schema_view = get_schema_view(
    openapi.Info(
        title="Car Dealer Marketplace API",
        default_version="v1",
        description="API documentation for the Car Dealer Marketplace",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#   API URL Patterns (Including Swagger)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("marketplace.urls")),  # Include API Endpoints
    #   Authentication Endpoints
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger UI
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="swagger-json"),
]
