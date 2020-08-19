from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views as v

urlpatterns = [
    path("", v.dashboard, name="dashboard"),
    path("my_conversation/", v.my_conversation, name="my_conversation"),
    path("settings/", v.settings, name="settings"),
    path(
        "chunks_speech_recognition/",
        v.chunks_speech_recognition,
        name="chunks_speech_recognition",
    ),
]
