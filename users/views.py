from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from tours.models import Tour
from bookings.models import VisaBooking,TourBooking


@login_required(login_url='login')
def dashboard(request):
    visa_bookings = VisaBooking.objects.all().filter(user=request.user).order_by('-id')
    tour_bookings = TourBooking.objects.all().filter(user=request.user).order_by('-id')
    total_bookings = tour_bookings.count()
    context = {
        'bookings': visa_bookings,
        'tour_bookings':tour_bookings,
    }
    return render(request, 'auth/dashboard/user-home.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'auth/dashboard/profile.html')

# @login_required(login_url='login')
# def chat(request):
#     return render(request, 'auth/dashboard/chat.html')

# @login_required(login_url='login')
# def my_favorites(request):
#     return render(request, 'auth/dashboard/my-favorites.html')



@login_required(login_url='login')
def view_order(request, pk):
    order =  get_object_or_404(Booking, pk=pk)
    context = {
        'order': order,
    }
    return render(request, 'auth/view-order.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('/')  # Or some other page

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                auth_login(request, user)  # Log the user in directly after registration
                return JsonResponse({
                    'success': True,
                    'message': f'Account created for {user.email}! You are now logged in.',
                    'redirect_url': reverse('index')  # Adjust the redirect URL as needed
                }, status=200)
            else:
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({'errors': errors}, status=400)
        except DatabaseError as e:
            # Handle database errors
            return JsonResponse({'success': False, 'error': "An error occurred. Please try again later!"}, status=500)
        except ValidationError as e:
            # Handle specific validation errors
            return JsonResponse({'success': False, 'error': "An error occurred. Please try again later!"}, status=400)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'success': False, 'error': "An unexpected error occurred!"}, status=500)
    
    else:
        form = SignUpForm()
    return render(request, 'auth/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            next_page = request.POST.get('next', '/')
            if url_has_allowed_host_and_scheme(next_page, allowed_hosts=settings.ALLOWED_HOSTS):
                return JsonResponse({'success': True, 'redirect_url': next_page})
            else:
                return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            return JsonResponse({'success': False, 'error': "Email or password is incorrect!"}, status=400)
            
    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get("q_Old_Password")
        new_password = request.POST.get("q_new_Password")
        confirmed_new_password = request.POST.get("q_confirm_new_Password")

        if old_password and new_password and confirmed_new_password:
            user = request.user
            if not user.check_password(old_password):
                messages.error(request, "Your old password is not correct!")
            elif new_password != confirmed_new_password:
                messages.error(request, "Your new password does not match the confirm password!")
            elif len(new_password) < 8 or new_password.lower() == new_password or \
                 new_password.upper() == new_password or new_password.isalnum() or \
                 not any(i.isdigit() for i in new_password):
                messages.error(request, "Your password is too weak!")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been changed successfully!")
                return redirect('change_password')
        else:
            messages.error(request, "Sorry, all fields are required!")

    return render(request, "auth/dashboard/profile.html")
        