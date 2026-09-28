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
    experiences = Experience.objects.all().order_by('-started_at')
    context = {
        'experiences': experiences,
        'name': 'Rania Aqila',
        'is_editor': is_editor_user(request.user),
        'is_superuser': is_superuser_user(request.user),
    }
    return render(request, "experience.html", context)


def show_works(request):
    title_query = request.GET.get('title', '')
    works = Work.objects.all()

    if title_query:
        works = works.filter(title__icontains=title_query)

    context = {
        'event_management': works.filter(category='event_management'),
        'writing': works.filter(category='writing'),
        'business_case': works.filter(category='business_case'),
        'product_management': works.filter(category='product_management'),
        'title_query': title_query,
        'name': 'Rania Aqila',
        'is_editor': is_editor_user(request.user),
        'is_superuser': is_superuser_user(request.user),
    }
    return render(request, "works.html", context)


@login_required(login_url='/login/')
def create_experience(request):
    # Server-side check: Hanya Superuser (Pemilik Portofolio)
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
    # Server-side check: Superuser ATAU Editor
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
    # Server-side check: Hanya Superuser
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
    data = Work.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_experience_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")