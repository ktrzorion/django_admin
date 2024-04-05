from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Blog, Like, Comment
from .serializers import CommentSerializer, BlogSerializer, LikesSerializer
from django.core.mail import send_mail
from django.db.models.functions import TruncMonth, TruncWeek, TruncQuarter, TruncYear
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime

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

# Weekly Chart
def blog_weekly_chart(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(weeks=1)

    blog_count_per_day = Blog.objects.filter(created_at__date__range=[start_date, end_date]) \
                                      .annotate(date=TruncWeek('created_at')) \
                                      .values('date') \
                                      .annotate(count=Count('id'))

    data = [{'date': entry['date'].strftime('%Y-%m-%d'), 'count': entry['count']} for entry in blog_count_per_day]

    return JsonResponse(data, safe=False)

# Monthly Chart
def blog_monthly_chart(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    blog_count_per_month = Blog.objects.filter(created_at__date__range=[start_date, end_date]) \
                                        .annotate(month=TruncMonth('created_at')) \
                                        .values('month') \
                                        .annotate(count=Count('id'))

    data = [{'month': entry['month'].strftime('%Y-%m'), 'count': entry['count']} for entry in blog_count_per_month]

    return JsonResponse(data, safe=False)

# Quarterly Chart
def blog_quarterly_chart(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)

    blog_count_per_quarter = Blog.objects.filter(created_at__date__range=[start_date, end_date]) \
                                         .annotate(quarter=TruncQuarter('created_at')) \
                                         .values('quarter') \
                                         .annotate(count=Count('id'))

    data = [{'quarter': entry['quarter'].strftime('%Y-%m-%d'), 'count': entry['count']} for entry in blog_count_per_quarter]

    return JsonResponse(data, safe=False)

# Yearly Chart
def blog_yearly_chart(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365*2)  # Consider two years for yearly chart

    blog_count_per_year = Blog.objects.filter(created_at__date__range=[start_date, end_date]) \
                                      .annotate(year=TruncYear('created_at')) \
                                      .values('year') \
                                      .annotate(count=Count('id'))

    data = [{'year': entry['year'].strftime('%Y'), 'count': entry['count']} for entry in blog_count_per_year]

    return JsonResponse(data, safe=False)