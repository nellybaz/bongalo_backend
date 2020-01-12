from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views


urlpatterns = [
    path('all', views.RegisterAPIView.as_view(), name="all_apartments"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
