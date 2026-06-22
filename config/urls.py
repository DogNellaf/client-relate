from django.contrib import admin
from django.urls import path

from crm.views import (
    home,
    register,
    login_view,
    logout_view,
    feedback_create,
    ticket_create,
    offer_create,
    my_interactions,
    notifications,
    hide_notification,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('feedback/new/', feedback_create, name='feedback_create'),
    path('ticket/new/', ticket_create, name='ticket_create'),
    path('offer/new/', offer_create, name='offer_create'),
    path('interactions/', my_interactions, name='my_interactions'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/hide/', hide_notification, name='hide_notification'),
]
