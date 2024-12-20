"""
URL configuration for aws_backend_project project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# The `schema_view` variable is being assigned the result of calling the `get_schema_view` function
# from the `drf_yasg` library. This function is used to generate a schema view for the API
# documentation.
schema_view = get_schema_view(
    openapi.Info(
        title="Open Delta APIs",
        default_version="1.0.0",
        description="This is a swagger for the Open Delta Rest APIs",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("opendelta_store.urls")),
    path(
        "swagger/schema/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger_view",
    ),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_URL)