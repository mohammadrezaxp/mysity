from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from blog.models import Category, Comments, Post
from blog.visibility import visible_posts

from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrStaff, IsStaffOrReadOnly
from .serializers import CategorySerializer, CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "auther", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_date", "counted_views"]
    ordering = ["-published_date", "-pk"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()
        return (
            visible_posts(self.request.user)
            .select_related("auther")
            .prefetch_related("category", "tag", "comment")
        )

    def perform_create(self, serializer):
        serializer.save(auther=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by("name", "pk")
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrStaff]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comments.objects.none()
        return (
            Comments.objects.filter(post__in=visible_posts(self.request.user))
            .select_related("author", "post")
            .order_by("creat_date", "pk")
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            name=serializer.validated_data.get("name")
            or self.request.user.get_full_name()
            or self.request.user.username,
            email=serializer.validated_data.get("email") or self.request.user.email,
        )
