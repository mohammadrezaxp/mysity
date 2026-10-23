from django.db import transaction
from rest_framework import serializers

from blog.content import clean_html
from blog.models import Category, Comments, Post
from blog.visibility import visible_posts


class SafeHTMLField(serializers.CharField):
    def to_internal_value(self, data):
        return clean_html(super().to_internal_value(data))

    def to_representation(self, value):
        return clean_html(value)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Comments
        fields = [
            "id",
            "post",
            "author",
            "name",
            "subject",
            "message",
            "email",
            "creat_date",
        ]
        read_only_fields = ["id", "author", "creat_date"]
        extra_kwargs = {"name": {"required": False}}

    def validate_post(self, value):
        if not visible_posts(self.context["request"].user).filter(pk=value.pk).exists():
            raise serializers.ValidationError("Post is not accessible.")
        if self.instance and value.pk != self.instance.post_id:
            raise serializers.ValidationError(
                "Comments cannot be moved to another post."
            )
        return value

    def validate_message(self, value):
        if len(value) > 10000:
            raise serializers.ValidationError("Comment is too long.")
        return value


class TagListField(serializers.ListField):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]


class PostSerializer(serializers.ModelSerializer):
    content = SafeHTMLField()
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        source="category",
        many=True,
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
    )
    comment = CommentSerializer(many=True, read_only=True)
    tag = TagListField(
        child=serializers.CharField(max_length=100), required=False, max_length=30
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "auther",
            "title",
            "content",
            "image",
            "counted_views",
            "category",
            "category_ids",
            "comment",
            "status",
            "tag",
            "login_re",
            "published_date",
            "created_date",
            "updated_date",
        ]
        read_only_fields = [
            "id",
            "auther",
            "counted_views",
            "created_date",
            "updated_date",
        ]

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop("tag", [])
        instance = super().create(validated_data)
        instance.tag.set(tags)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop("tag", None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tag.set(tags)
        return instance
