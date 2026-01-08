"""
Frontend views for rendering HTML templates.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


def landing_page(request):
    """Render landing page."""
    return render(request, 'landing.html')


@login_required
def superuser_dashboard(request):
    """Render superuser dashboard."""
    if not request.user.is_superuser:
        return redirect('landing')
    return render(request, 'superuser_dashboard.html')


@login_required
def gym_admin_dashboard(request):
    """Render gym admin dashboard."""
    if not request.user.is_gym_admin or not request.user.gym:
        return redirect('landing')
    return render(request, 'gym_admin_dashboard.html')


def login_page(request):
    """Render login page."""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('superuser_dashboard')
        elif request.user.is_gym_admin:
            return redirect('gym_admin_dashboard')
        return redirect('landing')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('superuser_dashboard')
            elif user.is_gym_admin:
                return redirect('gym_admin_dashboard')
            return redirect('landing')
    
    return render(request, 'login.html')
