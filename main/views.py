from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience, Work


def show_main(request):
    context = {
        "name": "Rania Aqila",
        "nickname": "nia",
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

def show_works(request):
    context = {
        "name": "Rania Aqila",
        "event_management": Work.objects.filter(category="event_management").order_by("-year"),
        "writing": Work.objects.filter(category="writing").order_by("-year"),
        "business_case": Work.objects.filter(category="business_case").order_by("-year"),
        "product_management": Work.objects.filter(category="product_management").order_by("-year"),
    }
    return render(request, "works.html", context)
