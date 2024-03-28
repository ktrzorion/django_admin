from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Blog, Like, Comment
from .serializers import CommentSerializer, BlogSerializer, LikesSerializer
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

class BlogsView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, *args, **kwargs):
        tags = request.GET.get('tags', None)

        if tags:
            blogs = Blog.objects.filter(comment__tags__icontains=tags).distinct()
        else:
            blogs = Blog.objects.all()

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class LikesView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        likes = Like.objects.all()
        serializer = LikesSerializer(likes, many=True)
        return Response(serializer.data)

class LikeView(APIView):

    def post(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)

        serializer = LikesSerializer(data={'user': request.user.id, 'blog': blog.id})
        
        if serializer.is_valid():
            like = serializer.save()

            user_email = blog.author.email
            blog_title = blog.title

            schedule_like_notification(user_email, blog_title)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        request.data['author'] = user.id
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            blog = serializer.save()
            return Response({'msg':'Blog Uploaded Successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentsView(APIView):

    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs.get('blog_id')
        tags = request.GET.get('tags', None)
        
        if tags:
            comments = Comment.objects.filter(blog__id=blog_id, tags__icontains=tags)
        else:
            comments = Comment.objects.filter(blog__id=blog_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentWriteView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        blog_id = kwargs.get('pk')
        request.data['user'] = user.id
        request.data['blog'] = blog_id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# SENDING EMAIL FOR LIKE
    
scheduler = BackgroundScheduler()
scheduler.start()

def send_like_notification_email(user_email, blog_title):
    subject = 'You got a like on your blog!'
    message = f'Your blog "{blog_title}" received a like. Check it out!'
    from_email = 'ktrzorion@gmail.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def schedule_like_notification(user_email, blog_title):
    run_time = datetime.now() + timedelta(minutes=1)

    scheduler.add_job(
        send_like_notification_email,
        'date',
        run_date=run_time,
        args=[user_email, blog_title],
        id=f'{user_email}_{blog_title}'
    )

def blog_chart(request):
    # Calculate the date range for the last 7 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    # Query to get the count of blogs added per day
    blog_count_per_day = Blog.objects.filter(created_at__date__range=[start_date, end_date]) \
        .extra({'created_at_day': 'date(created_at)'}) \
        .values('created_at_day') \
        .annotate(blog_count=Count('id'))

    # Prepare data for the chart
    labels = [entry['created_at_day'].strftime('%Y-%m-%d') for entry in blog_count_per_day]
    data = [entry['blog_count'] for entry in blog_count_per_day]

    return render(request, '.antino_blog/adminui/templates/admin/summary_chart.html', {'labels': labels, 'data': data})