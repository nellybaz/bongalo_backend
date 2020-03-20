from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views


urlpatterns = [
    path('register', views.UserRegisterViews.as_view(), name="register_user"),
    path('login', views.LoginView.as_view(), name="login_user"),
    path('update', views.UserView.as_view(), name="update_user"),
    path('delete', views.DeleteView.as_view(), name="delete_user"),
    path('social/auth', views.SocialAuth.as_view(), name="social_auth"),
    path('user/verify', views.VerifyUserView.as_view(), name="verify_user"),
    path('user/profile', views.UserView.as_view(), name="user_profile"),
    path('user/update-profile-image', views.UpdateProfileImage.as_view(), name="update_profile_image"),
    path('user/update-payment', views.PaymentMethod.as_view(), name="update_payment"),
    path('user/get-payment', views.PaymentMethod.as_view(), name="get_payment"),
    path('verify-email', views.VerifyEmail.as_view(), name="verify_email")
]

urlpatterns = format_suffix_patterns(urlpatterns)
