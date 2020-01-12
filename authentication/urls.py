from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views


urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="register_user"),
    path('login/<str:username>', views.LoginAPIView.as_view(), name="login_user"),
    path('update/<str:username>', views.UpdateAPIView.as_view(), name="update_user"),


]

urlpatterns = format_suffix_patterns(urlpatterns)
