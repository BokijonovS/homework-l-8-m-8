from django.urls import path, include
from rest_framework import routers

from .views import BlogAPIView, CommentListCreateAPIView, LikeListCreateAPIView


router = routers.SimpleRouter()
router.register('blog', BlogAPIView)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/blog/<int:pk>/comment/', CommentListCreateAPIView.as_view()),
    path('v1/blog/<int:pk>/like/', LikeListCreateAPIView.as_view()),
]

