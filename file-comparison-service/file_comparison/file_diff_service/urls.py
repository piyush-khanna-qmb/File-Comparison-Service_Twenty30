# file_diff_service/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_files, name='upload_files'),
    path('difference/', views.show_difference, name='show_difference'),
    path('api/promote/', views.promote_file_content, name='promote_file_content'),
    path('promote/', views.promote_page, name='promote_page'),
]