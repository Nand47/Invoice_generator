from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'), 
    path('invoice_generator', views.invoice_list, name='invoice_list'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('<int:invoice_id>/add-items/', views.add_items, name='add_items'),
    path('<int:invoice_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
    path('register/', views.register, name='register'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('', views.home, name='home'),
]