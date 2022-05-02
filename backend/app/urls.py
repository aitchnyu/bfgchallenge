from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login),
    path('add_transaction', views.add_transaction),
    path('get_transactions', views.show_transactions),
    path('mark_paid', views.mark_paid),
]
