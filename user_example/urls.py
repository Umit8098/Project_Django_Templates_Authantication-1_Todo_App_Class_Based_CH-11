from django.urls import path
from .views import (
    home,
    register,
    special,
)
from django.contrib.auth import views as auth_views

app_name = 'user_example'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    
    # custom password_chage view and template
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change.html"), name="password_change"),
    
    path('special/', special, name='special'),
    
    # custom logout view and redirect
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
]