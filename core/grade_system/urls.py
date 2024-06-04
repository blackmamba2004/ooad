from django.urls import path
from . import views

app_name = 'grade_system'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('accountant_dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('', views.main_page, name='main_page'),
    path('technologies_stack/', views.technologies_stack, name='technologies_stack'),
    path('accountant/calculate_coefficients/', views.calculate_coefficients, name='calculate_coefficients'),
    path('accountant/calculate_scholarship/', views.calculate_scholarship, name='calculate_scholarship'),
]
