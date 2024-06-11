from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Blog, Comment, Like
from .serializers import BlogSerializer, CommentSerializer,  LikeSerializer


class BlogAPIView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    

class CommentListCreateAPIView(APIView):
    
    def get_blog(self, pk: int):
        try:
            blog = Blog.objects.get(pk=pk)
            return blog
        except Blog.DoesNotExist:
            return Response({"detail": "Object doesn't exist"})
    
    def post(self, request: Request, pk: int):
        blog = self.get_blog(pk=pk)
        data = {
            'user': request.user.id,
            'blog': pk,
            'content': request.data['content']
        }
        serialzier = CommentSerializer(data=data)
        if serialzier.is_valid(raise_exception=True):
            serialzier.save()
            return Response({"data": serialzier.data})
    
    def get(self, request: Request, pk: int):
        blog = self.get_blog(pk=pk)
        comments = Comment.objects.filter(blog=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response({'data': serializer.data})
        
        
class LikeListCreateAPIView(APIView):
    def get_blog(self, pk: int):
        try:
            blog = Blog.objects.get(pk=pk)
            return blog
        except Blog.DoesNotExist:
            return None
    
    def is_alredy_liked(self, user, blog: Blog):
        try:
            like = Like.objects.get(user=user, blog=blog)
        except Like.DoesNotExist:
            return None
        else:
            return like
        
    def post(self, request: Request, pk: int):
        blog = self.get_blog(pk=pk)
        like = self.is_alredy_liked(request.user, blog)
        if like:
            like.delete()
            return Response({'detail': 'Like Removed'})
        else:
            data = {
                'user': request.user.id,
                'blog': blog.pk
            }
            serializer = LikeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'data': serializer.data})
    
    def get(self, request: Request, pk: int):
        blog = self.get_blog(pk)
        likes = Like.objects.filter(blog=blog)
        serializer = LikeSerializer(likes, many=True)
        return Response({'data': serializer.data})
        