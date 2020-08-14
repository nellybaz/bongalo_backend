from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [path('pay/confirm', views.PaymentView.as_view(), name="make_payment"), ]

urlpatterns = format_suffix_patterns(urlpatterns)
