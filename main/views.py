import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.core import serializers
from django.urls import reverse

from main.models import Work, Experience
from main.forms import WorkForm, ExperienceForm

from django.http import JsonResponse


def is_editor_user(user):
    return user.is_authenticated and user.groups.filter(name='Editor').exists()

def is_superuser_user(user):
    return user.is_authenticated and user.is_superuser

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum pernah login')
    context = {
        'name': 'Rania Aqila',
        'nickname' : 'Nia',
        'npm' : '2506623282',
        'study_program': "Information System",
        'last_login': last_login,
        'is_editor': is_editor_user(request.user),
        'is_superuser': is_superuser_user(request.user),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        'name': 'Rania Aqila',
        'is_editor': is_editor_user(request.user),
        'is_superuser': is_superuser_user(request.user),
        'form': ExperienceForm(),
    }
    return render(request, "experience.html", context)


def show_works(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rania Aqila",
        "title_query": title_query,
        "form": WorkForm(),
    }
    return render(request, "works.html", context)


@login_required(login_url='/login/')
def create_experience(request):
    if not is_superuser_user(request.user):
        return HttpResponseForbidden("403 Forbidden: Hanya Pemilik Portofolio (Superuser) yang dapat menambahkan Experience.")

    form = ExperienceForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {'form': form, 'is_edit': False, 'name': 'Rania Aqila'}
    return render(request, 'experience_form.html', context)


@login_required(login_url='/login/')
def update_experience(request, experience_id):
    if not (is_superuser_user(request.user) or is_editor_user(request.user)):
        return HttpResponseForbidden("403 Forbidden: Anda tidak memiliki akses Editor/Superuser untuk mengubah Experience.")

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {'form': form, 'is_edit': True, 'experience': experience, 'name': 'Rania Aqila'}
    return render(request, 'experience_form.html', context)


@login_required(login_url='/login/')
def delete_experience(request, experience_id):
    if not is_superuser_user(request.user):
        return HttpResponseForbidden("403 Forbidden: Hanya Pemilik Portofolio (Superuser) yang dapat menghapus Experience.")

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        return redirect('main:show_experience')

    return HttpResponseForbidden("403 Forbidden: Metode request tidak diizinkan.")


@login_required(login_url='/login/')
def create_work(request):
    if not is_superuser_user(request.user):
        return HttpResponseForbidden("403 Forbidden: Hanya Pemilik Portofolio (Superuser) yang dapat menambahkan Work.")

    form = WorkForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_works')

    context = {'form': form, 'is_edit': False, 'name': 'Rania Aqila'}
    return render(request, 'works_form.html', context)


@login_required(login_url='/login/')
def update_work(request, work_id):
    if not (is_superuser_user(request.user) or is_editor_user(request.user)):
        return HttpResponseForbidden("403 Forbidden: Anda tidak memiliki akses Editor/Superuser untuk mengubah Work.")

    work = get_object_or_404(Work, pk=work_id)
    form = WorkForm(request.POST or None, instance=work)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_works')

    context = {'form': form, 'is_edit': True, 'work': work, 'name': 'Rania Aqila'}
    return render(request, 'works_form.html', context)


@login_required(login_url='/login/')
def delete_work(request, work_id):
    if not is_superuser_user(request.user):
        return HttpResponseForbidden("403 Forbidden: Hanya Pemilik Portofolio (Superuser) yang dapat menghapus Work.")

    work = get_object_or_404(Work, pk=work_id)
    if request.method == "POST":
        work.delete()
        return redirect('main:show_works')

    return HttpResponseForbidden("403 Forbidden: Metode request tidak diizinkan.")


@login_required(login_url='/login/')
@require_POST
def toggle_star(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    if request.user in work.starred_by.all():
        work.starred_by.remove(request.user)
    else:
        work.starred_by.add(request.user)
    
    return redirect(request.META.get('HTTP_REFERER', 'main:show_works'))


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('main:login')

    context = {'form': form, 'name': 'Rania Aqila'}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm(request)

    context = {'form': form, 'name': 'Rania Aqila'}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def get_works_json(request):
    title_query = request.GET.get("title", "").strip()
    works = Work.objects.prefetch_related('starred_by').all().order_by("-year")

    if title_query:
        works = works.filter(title__icontains=title_query)

    data = []
    for work in works:
        starred_users = work.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(work.id),
            "fields": {
                "title": work.title,
                "category": work.category,
                "category_display": work.get_category_display(),
                "year": work.year,
                "photo_bw": work.photo_bw,
                "photo_color": work.photo_color,
                "project_image_url": work.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by('-started_at')

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "organization": experience.organization,
                "period": experience.period,
                "description": experience.description,
                "category": experience.category,
                "category_display": experience.get_category_display(),
            }
        })

    return JsonResponse(data, safe=False)

@require_POST
def create_experience_ajax(request):
    if not is_superuser_user(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_work_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = WorkForm(request.POST)
    if form.is_valid():
        work = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(work.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)