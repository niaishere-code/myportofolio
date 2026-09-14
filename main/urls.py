from django.urls import path

from main.views import show_main, show_experience, show_works

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("works/", show_works, name="show_works"),
]