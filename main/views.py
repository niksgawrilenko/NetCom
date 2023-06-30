from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.forms import RegistrationForm
from django.contrib.auth import get_user_model
from main.models import Subscriber, Package, Additional, Channel, TVPackage, Equipment
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from django.conf.urls.static import static
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import ModelBackend
def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Получение данных из формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            package = form.cleaned_data['package']
            tv_package = form.cleaned_data['tv_package']
            password = form.cleaned_data['password']

            # Создание и сохранение пользователя в базе данных
            user = form.save(commit=False)
            user.username = email
            user.balance = 0  # Установка значения balance в 0
            user.save()

            user.backend = 'main.backends.EmailBackend'

            # Аутентификация пользователя
            authenticated_user = authenticate(username=user.username, password=password)
            login(request, authenticated_user, backend='main.backends.EmailBackend')

            # Перенаправление на страницу успешной регистрации
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')



def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            subscriber = Subscriber.objects.get(email=email)
            if password == subscriber.password:
                user_profile_url = reverse('user_profile', kwargs={'subscriber_id': subscriber.pk})
                return redirect(user_profile_url)
            else:
                error_message = "Invalid email or password"
        except Subscriber.DoesNotExist:
            error_message = "Invalid email or password"
        context = {'error_message': error_message}
        return render(request, 'main/login.html', context)
    else:
        return render(request, 'main/login.html')



def user_profile(request, subscriber_id):
    subscriber = Subscriber.objects.get(pk=subscriber_id)
    payment_success = False

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        subscriber.balance += amount
        subscriber.save()
        payment_success = True
        return redirect('user_profile', subscriber_id=subscriber_id)

    context = {
        'subscriber': subscriber,
        'payment_success': payment_success
    }
    return render(request, 'main/user_profile.html', context)

def internet(request):
    packages = Package.objects.all()[1:]
    additional_services = Additional.objects.all()[1:9]
    return render(request, 'main/internet.html', {'packages': packages, 'additional_services': additional_services})

def tv(request):
    tv_packages = TVPackage.objects.all()
    channels = Channel.objects.all()
    return render(request, 'main/tv.html', {'tv_packages': tv_packages, 'channels': channels})


def equipment(request):
    equipment = Equipment.objects.all()
    return render(request, 'main/equipment.html', {'equipment': equipment})