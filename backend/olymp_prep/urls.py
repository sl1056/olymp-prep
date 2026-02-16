
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('tasks.urls')),
    path('api/pvp/', include('pvp.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/training/', include('training.urls')),
    path('api/', include('badges.urls')),
]
