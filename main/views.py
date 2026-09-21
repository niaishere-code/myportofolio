from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import WorkForm, ExperienceForm
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

def show_works(request):
    json_response = get_works_json(request)

    works = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    works = [work.object for work in works]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Nia",
        "works_list": works,
        "event_management": [w for w in works if w.category == "event_management"],
        "writing": [w for w in works if w.category == "writing"],
        "business_case": [w for w in works if w.category == "business_case"],
        "product_management": [w for w in works if w.category == "product_management"],
        "title_query": title_query,
    }
    return render(request, "works.html", context)

def create_work(request):
    form = WorkForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_works")

    context = {
        "name": "Nia",
        "form": form,
    }
    return render(request, "works_form.html", context)

def get_works_json(request):
    title_query = request.GET.get("title", "").strip()
    works = Work.objects.all()

    if title_query:
        works = works.filter(title__icontains=title_query)

    works_json = serializers.serialize("json", works)
    return HttpResponse(works_json, content_type="application/json")

def update_work(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    form = WorkForm(request.POST or None, instance=work)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Work berhasil diperbarui!")
        return redirect("main:show_works")

    context = {
        "name": "Rania Aqila",
        "form": form,
        "is_edit": True,
        "work": work,
    }
    return render(request, "works_form.html", context)

def delete_work(request, work_id):
    work = get_object_or_404(Work, pk=work_id)

    if request.method == "POST":
        work.delete()
        messages.success(request, "Work berhasil dihapus!")

    return redirect("main:show_works")


def show_experience(request):
    json_response = get_experience_json(request)
   
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()
   
    context = {
        "name": "Nia",
        "experience_list": experiences,  
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Rania Aqila",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Rania Aqila",
        "form": form,
        "is_edit": True,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")

    return redirect("main:show_experience")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")