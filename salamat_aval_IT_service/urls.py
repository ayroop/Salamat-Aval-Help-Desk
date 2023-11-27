from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('helpdesk.urls')),  # Include 'helpdesk' URLs under 'api/' prefix
]
