from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import WorkForm
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
        "title_query": title_query,
    }
    return render(request, "works.html", context)

def create_works(request):
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

def delete_work(request, work_id):
    work = get_object_or_404(Work, pk=work_id)

    if request.method == "POST":
        work.delete()
        messages.success(request, "Work berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")