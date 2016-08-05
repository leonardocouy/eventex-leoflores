from django.shortcuts import render
from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    form = SubscriptionForm()
    context = {
        'form': form
    }
    return render(request, 'subscriptions/subscription_form.html', context)