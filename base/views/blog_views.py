from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from base.models import Blog,Comment
from base.serializers.blog_serializers import BlogSerializer,BlogCommentSerializer




@api_view(['GET'])
def BlogList(request):
    blog = Blog.objects.all()
    serializer = BlogSerializer(blog, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([MultiPartParser,FormParser])
def createBlog(request):
    profile = request.user.profile
    data = request.data
    blog = Blog.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        author=profile,
        featured_image=data.get('image')
    )

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def BlogDetails(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateBlog(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.profile != blog.author:
        return Response({'message': 'You do not have permission to update this blog'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    blog.title = data.get('title', blog.title)
    blog.content = data.get('content', blog.content)
    blog.featured_image = data.get('image', blog.featured_image)
    blog.save()

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.profile != blog.author:
        return Response({'message': 'You do not have permission to delete this blog'}, status=status.HTTP_403_FORBIDDEN)

    blog.delete()
    return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#comments 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CommentOnblog(request):
    data = request.data
    profile = request.user.profile
    blogId = data.get('slug')
    try:
        blog = get_object_or_404(Blog, slug=blogId)
        # Check if the user has already commented on this blog
        if Comment.objects.filter(blog=blog, profile=profile).exists():
            return Response({'message': 'You have already commented on this blog.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            profile=profile,
            blog=blog,
            content=data.get('content')
        )
      

        serializer = BlogCommentSerializer(comment, many=False)
        return Response(serializer.data)
    except:
        return Response({'message': "Blog does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getBlogComments(request, slug):
    try:
        blog= get_object_or_404(Blog, slug=slug)
        comment =   Comment.objects.filter(blog=blog)
        serializer = BlogCommentSerializer(comment, many=True)
        return Response(serializer.data,)
    except:

        return Response({"mesage":"Blog doesnt exist"}, status=status.HTTP_404_NOT_FOUND)



 