from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from crm.models import Notification, Interaction
from crm.forms import InteractionForm, CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        form.set_type('feedback')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
    else:
        form = InteractionForm()
    return render(request, 'interaction_form.html', {
        'form': form,
        'title': 'Обратная связь',
        'submit_url': 'feedback_create',
    })


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        form.set_type('ticket')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
    else:
        form = InteractionForm()
    return render(request, 'interaction_form.html', {
        'form': form,
        'title': 'Добавить тикет',
        'submit_url': 'ticket_create',
    })


@login_required
def offer_create(request):
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        form.set_type('proposal')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
    else:
        form = InteractionForm()
    return render(request, 'interaction_form.html', {
        'form': form,
        'title': 'Внести предложение',
        'submit_url': 'offer_create',
    })


@login_required
def my_interactions(request):
    interaction_type = request.GET.get('type', '')
    qs = Interaction.objects.filter(user=request.user)
    if interaction_type in ('feedback', 'ticket', 'proposal'):
        qs = qs.filter(type=interaction_type)
    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'my_interactions.html', {
        'page_obj': page,
        'current_type': interaction_type,
    })


@login_required
def notifications(request):
    qs = Notification.objects.filter(user=request.user, is_hidden=False)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'notifications.html', {'page_obj': page})


@login_required
def hide_notification(request):
    if request.method != 'POST':
        return redirect('notifications')
    notification = get_object_or_404(Notification, pk=request.POST.get('id'))
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.is_hidden = True
    notification.save()
    return redirect('notifications')
