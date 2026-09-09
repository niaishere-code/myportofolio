from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "nia",
        "npm": "2506623282",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Information System Student, Universitas Indonesia "
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rania Aqila",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
