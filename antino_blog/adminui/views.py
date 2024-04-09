from django.shortcuts import render
from django.http import FileResponse

def weekly_report(request):
    file_path = '/home/ktr_zorion/Downloads/Antino Blogging Proj/antino_blog/adminui/templates/admin/weekly_summary.html'
    return FileResponse(open(file_path, 'rb'), content_type='text/html')

def monthly_report(request):
    file_path = '/home/ktr_zorion/Downloads/Antino Blogging Proj/antino_blog/adminui/templates/admin/monthly_summary.html'
    return FileResponse(open(file_path, 'rb'), content_type='text/html')

def quaterly_report(request):
    file_path = '/home/ktr_zorion/Downloads/Antino Blogging Proj/antino_blog/adminui/templates/admin/quaterly_summary.html'
    return FileResponse(open(file_path, 'rb'), content_type='text/html')

def yearly_report(request):
    file_path = '/home/ktr_zorion/Downloads/Antino Blogging Proj/antino_blog/adminui/templates/admin/yearly_summary.html'
    return FileResponse(open(file_path, 'rb'), content_type='text/html')