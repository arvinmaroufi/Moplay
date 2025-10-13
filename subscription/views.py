from django.shortcuts import render
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription


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
