from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apartment import views


urlpatterns = [
    path('add', views.ApartmentCreateAPIView.as_view(), name="add_apartment"),
    path('update/<str:uid>', views.ApartmentUpdateDeleteAPIView.as_view(), name="update_apartment"),
    path('delete/<str:uid>', views.ApartmentUpdateDeleteAPIView.as_view(), name="delete_apartment"),
    path('all', views.ApartmentListAPIView.as_view(), name="all_apartments"),
    path('search', views.ApartmentSearchAPIView.as_view(), name="search_apartments"),
    path('review/create', views.ReviewListUpdateCreate.as_view(), name="search_apartments"),
    path('review/delete', views.ReviewListUpdateCreate.as_view(), name="search_apartments"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
