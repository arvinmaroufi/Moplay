from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def subscription_plans(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)

    context = {
        'plans': plans,
        'active_plan': None
    }

    if request.user.is_authenticated:
        active_subscription = UserSubscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()
        context['active_plan'] = active_subscription.plan if active_subscription else None

    return render(request, 'subscription/plans.html', context)


@login_required
def select_plan(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    # check if the user has an active subscription
    active_subscription = UserSubscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if active_subscription:
        messages.warning(request, 'شما در حال حاضر اشتراک فعال دارید')
        return redirect('subscription:plans')

    if request.method == 'POST':
        # checking the type of payment
        payment_method = request.POST.get('payment_method')

        # create a new subscription
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            payment_amount=plan.price,
            status='pending'
        )

        if payment_method == 'wallet':
            # pay with wallet
            wallet = request.user.wallet

            if wallet.balance >= plan.price:
                # deduct from wallet
                wallet.withdraw(plan.price)

                # enable subscription
                subscription.status = 'active'
                subscription.save()

                # create a payment record
                Payment.objects.create(
                    user=request.user,
                    subscription=subscription,
                    amount=plan.price,
                    status='completed',
                    payment_date=timezone.now()
                )

                messages.success(request, f'اشتراک {plan.name} با موفقیت با کیف پول فعال شد')
                return redirect('subscription:subscription_detail', subscription_id=subscription.id)
            else:
                # delete pending subscription because payment failed
                subscription.delete()
                messages.error(request, 'موجودی کیف پول شما کافی نیست')
                return redirect('subscription:select_plan', plan_id=plan_id)

        else:
            # direct payment (payment gateway)
            # here the user should be redirected to the payment gateway
            # for example, we directly activate the status
            subscription.status = 'active'
            subscription.save()

            # create a payment record
            Payment.objects.create(
                user=request.user,
                subscription=subscription,
                amount=plan.price,
                status='completed',
                payment_date=timezone.now()
            )

            messages.success(request, f'اشتراک {plan.name} با موفقیت فعال شد')
            return redirect('subscription:subscription_detail', subscription_id=subscription.id)

    # get user wallet balance
    wallet_balance = request.user.wallet.balance if hasattr(request.user, 'wallet') else 0

    context = {
        'plan': plan,
        'active_subscription': active_subscription,
        'wallet_balance': wallet_balance
    }
    return render(request, 'subscription/select_plan.html', context)
