from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('internet', views.internet, name="internet"),
    path('tv', views.tv, name="tv"),
    path('equipment', views.equipment, name="equipment"),
    path('register', views.register, name="register"),
    path('login/', views.login_user, name='login'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('user_profile/<int:subscriber_id>/', views.user_profile, name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout')
]
