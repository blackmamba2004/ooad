from django.urls import path
from . import views

app_name = 'grade_system'

urlpatterns = [
    path('', views.panel_grade, name='panel_grade'),
    path('login/', views.login_user, name='login'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
]
