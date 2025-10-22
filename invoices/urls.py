from django.urls import path
from . import views



urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('<int:invoice_id>/add-items/', views.add_items, name='add_items'),
    path('<int:invoice_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
]