from rest_framework import serializers
from base.serializers.auth_serializers import ProfileSerializer
from base.models import Blog,Comment



class BlogSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Blog
        fields = "__all__"



class BlogCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Comment
        fields = "__all__"