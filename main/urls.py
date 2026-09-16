from django.urls import path

from main.views import delete_work, get_works_json, show_main, show_experience, show_works, create_works

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("works/", show_works, name="show_works"),
    path("works/create/", create_works, name="create_works"),
    path("works/json/", get_works_json, name="get_works_json"),
    path("works/<uuid:work_id>/delete/",delete_work,name="delete_work"),
    path("api/works/", get_works_json, name="get_works_json"),
]