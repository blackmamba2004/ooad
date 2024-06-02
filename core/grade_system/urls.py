from django.urls import path
from . import views

app_name = 'grade_system'

urlpatterns = [
    path('panel_grade/', views.panel_grade, name='panel_grade'),
    path('login/', views.login_user, name='login'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('', views.main_page, name='main_page'),
    path('technologies_stack/', views.technologies_stack, name='technologies_stack')
]
