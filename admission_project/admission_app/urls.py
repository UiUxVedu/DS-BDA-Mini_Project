from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_data, name='add'),
    path('predict/', views.predict, name='predict'),
    path('analytics/', views.analytics, name='analytics'),
    path('history/', views.history, name='history'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
]