from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    # path('book', views.PaymentView.as_view(), name="make_booking"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
