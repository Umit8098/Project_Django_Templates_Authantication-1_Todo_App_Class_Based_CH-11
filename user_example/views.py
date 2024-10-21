from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'user_example/index.html')

#! register -> login edip -> home page 
# def register(request):
#     form = UserCreationForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password1")
#         user = authenticate(username = username, password = password)
#         # return redirect('user_example:login')
#         login(request, user)
#         return redirect('user_example:home')
#     context = {
#         'form': form
#     }
#     return render(request, 'registration/register.html', context)

#! register -> login page 
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


# @login_required
def special(request):
    return render(request, 'user_example/special.html')
