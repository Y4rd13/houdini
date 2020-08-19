"""houdini_proyect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
--------------------------------------------------------------------------------
# To re-create the missing Site object from shell:
    from django.contrib.sites.models import Site
    Site.objects.create(pk=1, domain='www.example.com', name='example.com')
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import url
from houdini_app import views as v
from dashboard import urls
from django.conf import settings
from django.views.generic import TemplateView
from dashboard import views as d
from zoom import views as z

urlpatterns = [
    path("admin/", admin.site.urls),  # admin
    path("accounts/", include("allauth.urls")),  # allauth
    url(
        r"^favicon\.ico$",
        RedirectView.as_view(url="/static/images/login/icons/favicon.ico"),
    ),
    path("", v.index, name="index"),
    path("dashboard/", include("dashboard.urls"), name="dashboard"),
    path("login/", v.loginPage, name="login"),
    path("zoom/", v.zoom, name="zoom"),
    path("meeting.html", v.meeting, name="meeting"),
    path("speech/", v.speech, name="speech"),
    path("delete_document/<int:docid>/", d.delete_document, name="delete_document"),
    path("testzoom/", v.testrequest),
    path("requestzoom/", z.requestInfo),
]

settings.APPEND_SLASH = False
