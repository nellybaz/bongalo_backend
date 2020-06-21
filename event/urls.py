from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from event import views


urlpatterns = [
    path(
        'all',
        views.EventView.as_view(),
        name="get_all_events"),

    path(
        'get',
        views.SingleEventView.as_view(),
        name="get_an_event"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
