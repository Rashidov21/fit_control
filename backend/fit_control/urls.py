"""
URL configuration for fit_control project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views_frontend import landing_page, superuser_dashboard, gym_admin_dashboard, login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login_page'),
    path('superuser/', superuser_dashboard, name='superuser_dashboard'),
    path('gym-admin/', gym_admin_dashboard, name='gym_admin_dashboard'),
    path('api/auth/', include('core.urls')),
    path('api/superuser/', include('gyms.superuser_urls')),
    path('api/gym/', include('gyms.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
