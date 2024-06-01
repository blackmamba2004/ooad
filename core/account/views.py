# from django.shortcuts import render
# from .forms import LoginForm
# from django.db import connection
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
#
# from ..grade_system.models import Teacher, Discipline
#
#
# def get_teacher_disciplines(teacher):
#     disciplines = Discipline.objects.filter(
#         speciality_discipline__teacher_discipline__teacher=teacher
#     ).distinct()
#     return disciplines.values_list('title', flat=True)
#
#
# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     # Проверка, является ли пользователь преподавателем
#                     try:
#                         teacher = Teacher.objects.get(user=user)
#                         disciplines = get_teacher_disciplines(teacher)
#                         # Возвращаем дисциплины преподавателя
#                         return render(request, 'account/teacher_dashboard.html', {'disciplines': disciplines})
#                     except Teacher.DoesNotExist:
#                         return HttpResponse('Вы не являетесь преподавателем!')
#                 else:
#                     return HttpResponse('Ваша запись отключена!')
#             else:
#                 return HttpResponse('Недопустим вход!')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login_form.html', {'form': form})
