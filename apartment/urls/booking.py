from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apartment import views

urlpatterns = [
    path(
        'book',
        views.CreateBookingView.as_view(),
        name="book_apartment"),

    path('<uuid>/cancel',
         views.RetrieveDeleteBookingDetailsAPIView.as_view(),
         name='cancel_booking'),
    path('',
         views.MyBooking.as_view(),
         name='my_booking')]

urlpatterns = format_suffix_patterns(urlpatterns)