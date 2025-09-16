from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User, VerificationCode
from django.utils import timezone
from .utils import send_verification_email
from django.contrib.auth import login as auth_login, logout as auth_logout


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


def login(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']

            request.session['pending_user_id'] = user.id
            request.session['pending_user_email'] = user.email
            request.session['pending_user_created_at'] = str(timezone.now())

            verification_code = VerificationCode.generate_code(user)
            send_verification_email(user, verification_code.code)

            messages.info(request, 'کد تایید به ایمیل شما ارسال شد')
            return redirect('accounts:verify_code')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    auth_logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('core:home')


def verify_code(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    user_id = request.session.get('pending_user_id')
    user_email = request.session.get('pending_user_email')
    verification_created_at = request.session.get('pending_user_created_at')

    if not user_id or not user_email or not verification_created_at:
        messages.error(request, 'لطفا ابتدا اطلاعات ورود را وارد کنید')
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id, email=user_email)
    except User.DoesNotExist:
        if 'pending_user_id' in request.session:
            del request.session['pending_user_id']
        if 'pending_user_email' in request.session:
            del request.session['pending_user_email']
        if 'pending_user_created_at' in request.session:
            del request.session['pending_user_created_at']

        messages.error(request, 'کاربر یافت نشد')
        return redirect('accounts:login')

    created_at = timezone.datetime.fromisoformat(verification_created_at)
    expiration_time = created_at + timezone.timedelta(minutes=2)
    remaining_time = max(0, (expiration_time - timezone.now()).total_seconds())

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        if remaining_time <= 0:
            VerificationCode.cleanup_expired_codes()

            if 'pending_user_id' in request.session:
                del request.session['pending_user_id']
            if 'pending_user_email' in request.session:
                del request.session['pending_user_email']
            if 'pending_user_created_at' in request.session:
                del request.session['pending_user_created_at']

            messages.error(request, 'زمان تایید کد به پایان رسیده است. لطفا مجددا تلاش کنید')
            return redirect('accounts:login')

        try:
            verification_code = VerificationCode.objects.get(user=user, code=code)

            if verification_code.is_valid():
                verification_code.mark_as_used()

                if 'pending_user_id' in request.session:
                    del request.session['pending_user_id']
                if 'pending_user_email' in request.session:
                    del request.session['pending_user_email']
                if 'pending_user_created_at' in request.session:
                    del request.session['pending_user_created_at']

                auth_login(request, user)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('core:home')
            else:
                verification_code.delete()

                if verification_code.is_used:
                    messages.error(request, 'این کد قبلا استفاده شده است')
                else:
                    messages.error(request, 'کد تایید منقضی شده است')

                    if 'pending_user_id' in request.session:
                        del request.session['pending_user_id']
                    if 'pending_user_email' in request.session:
                        del request.session['pending_user_email']
                    if 'pending_user_created_at' in request.session:
                        del request.session['pending_user_created_at']
                    return redirect('accounts:login')

        except VerificationCode.DoesNotExist:
            messages.error(request, 'کد تایید نامعتبر است')

    if remaining_time <= 0:
        if 'pending_user_id' in request.session:
            del request.session['pending_user_id']
        if 'pending_user_email' in request.session:
            del request.session['pending_user_email']
        if 'pending_user_created_at' in request.session:
            del request.session['pending_user_created_at']

        messages.error(request, 'زمان تایید کد به پایان رسیده است. لطفا مجددا تلاش کنید')
        return redirect('accounts:login')

    context = {
        'remaining_time': int(remaining_time),
        'user_email': user_email
    }

    return render(request, 'accounts/verify_code.html', context)
