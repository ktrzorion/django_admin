from django.contrib import admin
from django.urls import path, include
from adminui import views

admin.site.site_header = "-- Antino Blogging --"
admin.site.site_title = "Welcome to Antino Blogging"
admin.site.index_title = "Database Schema"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('api/', include('authapp.urls')),
    path('weekly-report/', views.weekly_report, name='weekly_report'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    path('quaterly-report/', views.quaterly_report, name='quaterly_report'),
    path('yearly-report/', views.yearly_report, name='yearly_report'),
]