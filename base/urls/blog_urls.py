from django.urls import path
from base.views import blog_views as views

urlpatterns = [
    path('list/', views.BlogList, name='list_blog'),
    path('create/', views.createBlog, name='create_blog'),
    path('details/<slug:slug>/', views.BlogDetails, name='blog_details'),
    path('update/<str:id>/', views.updateBlog, name='update_blog'),
    path('delete/<int:id>/', views.deleteBlog, name='delete_blog'),
    path('comment/', views.CommentOnblog ),
    path('comments/<slug:slug>/', views.getBlogComments)
]
