from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
