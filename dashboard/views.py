from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification, Wallet
from .forms import ProfileEditForm, ChangePasswordForm, WalletChargeForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from subscription.models import UserSubscription


@login_required
def mark_notification_as_read(request, notification_id):
    """
    Mark a notification as read by the current user

    Parameters:
        request: HTTP request object
        notification_id: ID of the notification to mark as read

    Returns:
        Redirect to dashboard with appropriate message
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        has_access = (
                notification.users.filter(id=request.user.id).exists() or
                notification.is_for_all_users
        )

        if has_access:
            notification.mark_as_read(request.user)
            messages.success(request, 'اعلان با موفقیت خوانده شد')
        else:
            messages.error(request, 'دسترسی غیرمجاز')

    except Notification.DoesNotExist:
        messages.error(request, 'اعلان یافت نشد')

    return redirect('dashboard:dashboard')


@login_required
def dashboard(request):
    user = request.user
    password_form = None
    profile_form = None
    wallet_form = None

    # Notification handling
    Notification.delete_expired_notifications()
    notifications = Notification.get_active_notifications_for_user(user)

    for notification in notifications:
        notification.is_read = notification.read_by.filter(id=user.id).exists()
        notification.is_recent = notification.created_at > (timezone.now() - timezone.timedelta(hours=24))

    recent_notifications_count = Notification.get_recent_notifications_count(user)

    # Get or create user wallet
    wallet, created = Wallet.objects.get_or_create(user=user)

    # Get active user subscription
    active_subscription = UserSubscription.objects.filter(user=user, status='active', end_date__gt=timezone.now()).first()

    # Handle POST requests
    if request.method == 'POST':
        # Profile editing form submission
        if 'edit_profile' in request.POST:
            profile_form = ProfileEditForm(request.POST, request.FILES)
            if profile_form.is_valid():
                # Update user profile data
                user.first_name = profile_form.cleaned_data['first_name']
                user.last_name = profile_form.cleaned_data['last_name']
                user.phone = profile_form.cleaned_data['phone']
                user.about_me = profile_form.cleaned_data['about_me']

                if 'profile_photo' in request.FILES:
                    user.profile_photo = request.FILES['profile_photo']

                user.save()

                messages.success(request, 'پروفایل شما با موفقیت به‌روزرسانی شد')
                return redirect('dashboard:dashboard')
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

        # Password change form submission
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.POST, user=user)
            if password_form.is_valid():
                # Update user password
                new_password = password_form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()

                auth_logout(request)
                messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت. لطفا با رمز عبور جدید وارد شوید')
                return redirect('accounts:login')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

        # Charge wallet
        elif 'charge_wallet' in request.POST:
            wallet_form = WalletChargeForm(request.POST)
            if wallet_form.is_valid():
                amount = wallet_form.cleaned_data['amount']
                # Increase wallet balance
                new_balance = wallet.deposit(amount)
                messages.success(request,
                                 f'کیف پول شما با موفقیت به مبلغ {amount:,} تومان شارژ شد. موجودی فعلی: {new_balance:,} تومان')
                return redirect('dashboard:dashboard')

    # Initialize profile form with current user data if not already set
    if profile_form is None:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'about_me': user.about_me
        }
        profile_form = ProfileEditForm(initial=initial_data)

    # Initialize password form if not already set
    if password_form is None:
        password_form = ChangePasswordForm()

    # Initialize wallet form if not already set
    if wallet_form is None:
        wallet_form = WalletChargeForm()

    context = {
        'user': user,
        'notifications': notifications,
        'recent_notifications_count': recent_notifications_count,
        'form': profile_form,
        'password_form': password_form,
        'wallet_form': wallet_form,
        'wallet': wallet,
        'active_subscription': active_subscription,
    }
    return render(request, 'dashboard/dashboard.html', context)
