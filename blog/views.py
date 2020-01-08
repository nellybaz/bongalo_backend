from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from blog.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from blog.models import Post as BlogPost
from blog.serializers import PostSerializers
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, filters
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('snippet-list', request=request, format=format)
    })


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        fields_to_search = []
        if request.query_params.get('title'):
            fields_to_search.append('title')
        if request.query_params.get('body'):
            fields_to_search.append('body')

        return super(CustomSearchFilter, self).get_search_fields(view, request)\
            if not fields_to_search else fields_to_search


# Using Generics
class PostsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'body']


class PostDetail2(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializers


class SearchPost(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializers
    filter_backends = [CustomSearchFilter]
    search_fields = ['title', 'body']


class FilterPost(generics.ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        search_title = self.kwargs['name']
        search_body = self.kwargs['body']
        return BlogPost.objects.filter(title__contains=search_title, body__contains=search_body)


# Using class views
class PostDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializers(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Using mixin
class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def posts(request, format=None):
    """
    List all blog posts

    :param request:
    :param format:
    :return:
    """

    if request.method == "GET":
        blog_posts = BlogPost.objects.all()
        serializer = PostSerializers(blog_posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_details(request, pk, format=None):
    """
    Retrieve, update, delete a blog post
    :param request:
    :param pk:
    :param format:
    :return:
    """

    try:
        blog_post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializers(blog_post)
        Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializers(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
