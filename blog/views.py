from rest_framework import status
from rest_framework.response import Response
from blog.models import Post as BlogPost
from blog.serializers import BlogPostSerializers as PostSerializers
from rest_framework.views import APIView
from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        fields_to_search = []
        if request.query_params.get('title'):
            fields_to_search.append('title')
        if request.query_params.get('body'):
            fields_to_search.append('body')

        return super(CustomSearchFilter, self).get_search_fields(
            view, request) if not fields_to_search else fields_to_search


class BlogPostView(APIView):
    def get(self, request):
        query = BlogPost.objects.filter(is_active=True)
        serialized = PostSerializers(query, many=True)
        if serialized:
            response = {
                'responseCode': 1,
                'data': serialized.data,
                'message': 'Blog post data fetched successfully'
            }

            return Response(status=status.HTTP_200_OK, data=response)

        response = {
            'responseCode': 0,
            'message': 'Error occurred when fetching blog post'
        }

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=response)


class BlogSinglePostView(APIView):
    def get(self, request):
        blog_id = self.request.query_params.get('blog')
        if not BlogPost.objects.filter(is_active=True, uuid=blog_id).exists():
            response = {
                'responseCode': 0,
                'message': 'No blog found'
            }

            return Response(status=status.HTTP_404_NOT_FOUND, data=response)

        query = BlogPost.objects.get(is_active=True, uuid=blog_id)
        serialized = PostSerializers(query)
        if serialized:
            response = {
                'responseCode': 1,
                'data': serialized.data,
                'message': 'Blog post data fetched successfully'
            }

            return Response(status=status.HTTP_200_OK, data=response)

        response = {
            'responseCode': 0,
            'message': 'Error occurred when fetching blog post'
        }

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=response)
