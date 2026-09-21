from django.urls import path

from main.views import create_experience, delete_experience, delete_work, get_works_json, show_main, show_experience, show_works, create_work, update_experience, update_work, get_experience_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("works/", show_works, name="show_works"),
    path("works/add/", create_work, name="create_work"),
    path("works/<uuid:work_id>/edit/", update_work, name="update_work"),
    path("works/<uuid:work_id>/delete/", delete_work, name="delete_work"),
    path("api/works/", get_works_json, name="get_works_json"),
    path ("api/experience/", get_experience_json, name="get_experience_json")
]
