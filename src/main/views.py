from django.shortcuts import render, redirect
from .forms import RegisterForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import DiaryEntry
# Create your views here.


@login_required(login_url="/login")
def home(request):
    # TODO: need to add some user info and CHANGE home.html
    # TODO: create a separate page for admins - view everything that users are posting with ban option
    entries = DiaryEntry.objects.all()

    if request.method == 'POST':
        entry_id = request.POST.get("entry-id")
        entry = DiaryEntry.objects.filter(id=entry_id).first()
        if entry and entry.author == request.user:
            entry.delete()

    return render(request, 'main/home.html', {"entries": entries})

# TODO: add
# @login_required(login_url="/login")
# def diary_analytics(request):
#     return render(request, 'main/diary_analytics.html') # plot + history


@login_required(login_url="/login")
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = EntryForm()

    return render(request, 'main/create_entry.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
