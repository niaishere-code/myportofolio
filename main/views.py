import datetime

from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from main.forms import WorkForm, ExperienceForm
from main.models import Experience, Work

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rania",
        "npm": "2506623282",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
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


@login_required(login_url="/login/") 
def create_work(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Rania",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rania",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Work, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")