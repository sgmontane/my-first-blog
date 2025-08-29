from django.urls import path
from . import views

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('post/new/', views.post_new, name='post_new'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('', views.leaderboard, name='leaderboard'), #leaderboard
    path('submit/', views.submit_build_time, name='submit_build_time'), #submit build time form
    path('builder/<int:builder_id>/', views.builder_stats, name='builder_stats'),
    path('records/', views.subassembly_records, name='subassembly_records'),

]
