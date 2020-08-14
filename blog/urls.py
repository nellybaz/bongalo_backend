from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views


urlpatterns = [
    path(
        'posts/all',
        views.BlogPostView.as_view(),
        name="get_all_blog_post"),
    path(
        'posts/get',
        views.BlogSinglePostView.as_view(),
        name="get_single_post"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
