from django.urls import path
from . import  views
urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('job/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('post-job/', views.job_create_view, name='job_create'),
]