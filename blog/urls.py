from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views


urlpatterns = [
    path('posts/', views.posts),
    path('posts-generic/', views.PostsList.as_view()),
    path('posts-search-generic', views.SearchPost.as_view()),
    path('posts-filter-generic/<str:name>/<str:body>', views.FilterPost.as_view()),
    path('posts-generic/<int:pk>', views.PostDetail2.as_view()),
    path('posts-mixin/', views.PostList.as_view()),
    path('posts-new/<int:pk>', views.PostDetail.as_view()),
    path('posts/<int:pk>', views.post_details),
    path('post-details-class/<int:pk>', views.PostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
