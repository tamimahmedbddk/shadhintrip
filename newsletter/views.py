from django.shortcuts import render, redirect
from .forms import SubscriberForm

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscription_success')
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/subscribe.html', {'form': form})

def subscription_success(request):
    return render(request, 'newsletter/subscription_success.html')
