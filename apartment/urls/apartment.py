from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apartment import views


urlpatterns = [
    path(
        'add',
        views.ApartmentCreateAPIView.as_view(),
        name="add_apartment"),
    path(
        'update',
        views.ApartmentUpdateDeleteAPIView.as_view(),
        name="update_apartment"),
    path(
        'delete',
        views.ApartmentUpdateDeleteAPIView.as_view(),
        name="delete_apartment"),
    path(
        'get',
        views.ApartmentDetailsView.as_view(),
        name="get_apartment_details"),
    path(
        'all',
        views.ApartmentListAPIView.as_view(),
        name="all_apartments"),
    path(
        'search',
        views.ApartmentSearchAPIView.as_view(),
        name="search_apartments"),
    path(
        'review/add',
        views.ReviewListUpdateCreate.as_view(),
        name="add_apartment_review"),
    path(
        'review/delete',
        views.ReviewListUpdateCreate.as_view(),
        name="delete_apartment_review"),
    path(
        'review',
        views.ReviewListUpdateCreate.as_view(),
        name="get_apartment_review"),
    path(
        'images/add',
        views.ImageView.as_view(),
        name="add_apartment_image"),
    path(
        'images/get',
        views.ImageView.as_view(),
        name="get_apartment_image"),
    path(
        'book',
        views.CreateBookingView.as_view(),
        name="book_apartment"),
    path(
        'rate',
        views.RatingView.as_view(),
        name="rate_apartment"),
    path(
        'show-listing',
        views.ListingView.as_view(),
        name="show_listing"),
    path(
        'delete-listing',
        views.ListingView.as_view(),
        name="delete_listing"),
    path(
        'update-listing',
        views.ListingView.as_view(),
        name="update_listing"),
]

urlpatterns = format_suffix_patterns(urlpatterns)