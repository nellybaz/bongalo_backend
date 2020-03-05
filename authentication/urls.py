from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views


urlpatterns = [
    path('register', views.UserRegisterViews.as_view(), name="register_user"),
    path('login', views.LoginView.as_view(), name="login_user"),
    path('update', views.UserUpdateView.as_view(), name="update_user"),
    path('delete', views.DeleteView.as_view(), name="delete_user"),
    path('social/auth', views.SocialAuth.as_view(), name="social_auth"),
    path('user/verify', views.VerifyUserView.as_view(), name="verify_user"),




]

urlpatterns = format_suffix_patterns(urlpatterns)
