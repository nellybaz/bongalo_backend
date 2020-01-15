from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/apartment/', include('apartment.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]