from django.shortcuts import render, redirect
from .forms import RegisterForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import DiaryEntry
from .apps import MainConfig
import logging

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


@login_required(login_url="/login")
def home(request):
    # TODO: need to add some user info and CHANGE home.html
    # TODO: create a separate page for admins - view everything that users are posting with ban option
    entries = DiaryEntry.objects.filter(author=request.user).order_by('-created_at')

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
    logger = logging.getLogger('api/create_entry/')
    if request.method == 'POST':
        post_data = request.POST or None
        file_data = request.FILES or None

        form = EntryForm(post_data, file_data)
        if form.is_valid():
            
            post = form.save(commit=False)
            post.author = request.user

            model = MainConfig.model
            result = model.sentiment_predict(post.text)
            sentiment_score = result['score']
            sentiment_label = result['label']

            logger.info(f'user input text: {post.text} Model sentiment: {sentiment_score}')
            print(f'user input text: {post.text} Model sentiment: {sentiment_score}, {sentiment_label}')

            post.sentiment_score = sentiment_score
            post.sentiment_label = sentiment_label
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
