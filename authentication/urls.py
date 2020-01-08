from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('register/<str:username>', views.UpdateAPIView.as_view(), name="register_item"),
    path('profiles/', views.ProfileAPIView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
