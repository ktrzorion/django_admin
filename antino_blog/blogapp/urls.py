from django.urls import path
from .views import BlogsView, CommentsView, LikesView, BlogCreateView, CommentWriteView, LikeView, blog_weekly_chart, blog_monthly_chart, blog_quarterly_chart, blog_yearly_chart

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name='blog-list'),
    path('upload/blog/', BlogCreateView.as_view(), name='blog-list'),
    path('like/<int:pk>/', LikeView.as_view(), name='like'),
    path('blog/likes/<int:pk>', LikesView.as_view(), name='like'),
    path('comment/', CommentsView.as_view(), name='comment'),
    path('comment/<int:pk>/', CommentWriteView.as_view(), name='comment'),
    path('blog-weekly-chart/', blog_weekly_chart, name='blog_chart'),
    path('blog-monthly-chart/', blog_monthly_chart, name='blog_chart'),
    path('blog-quarterly-chart/', blog_quarterly_chart, name='blog_chart'),
    path('blog-yearly-chart/', blog_yearly_chart, name='blog_chart'),
]