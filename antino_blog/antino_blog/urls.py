from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "-- Antino Blogging --"
admin.site.site_title = "Welcome to Antino Blogging"
admin.site.index_title = "Database Schema"

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('api/', include('authapp.urls')),
]