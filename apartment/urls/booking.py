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
    path('my_bookings',
         views.MyBooking.as_view(),
         name='my_booking'),
    path('my_apartment_booking',
         views.BookingOnMyApartment.as_view(),
         name='booking_on_my_apartment')
]

urlpatterns = format_suffix_patterns(urlpatterns)