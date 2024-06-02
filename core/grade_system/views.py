from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Teacher, Discipline, Group, Student, Grade


def panel_grade(request):
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM grades WHERE group_name = '22-КБ-ПР1'""")
        data = cursor.fetchall()
        return render(request, "grade_system/student_grades.html", {'data': data})


def get_teacher_disciplines(teacher):
    disciplines = Discipline.objects.filter(
        speciality_discipline__teacher_discipline__teacher=teacher
    ).distinct()
    return disciplines


@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Проверка, является ли пользователь преподавателем
                    try:
                        teacher = Teacher.objects.get(user=user)

                        disciplines = list(get_teacher_disciplines(teacher))
                        # Сохранение дисциплин в сессии
                        # request.session['disciplines'] = disciplines
                        request.session['disciplines'] = [discipline.id for discipline in disciplines]
                        # Перенаправление на login/dashboard
                        return redirect('grade_system:teacher_dashboard')
                    except Teacher.DoesNotExist:
                        return HttpResponse('Вы не являетесь преподавателем!')
                else:
                    return HttpResponse('Ваша запись отключена!')
            else:
                return HttpResponse('Недопустим вход!')
    else:
        form = LoginForm()
    return render(request, 'grade_system/login_form.html', {'form': form})


@login_required
def dashboard(request):
    # Извлечение дисциплин из сессии
    disciplines = request.session.get('disciplines', [])
    return render(request, 'grade_system/teacher_dashboard.html', {'disciplines': disciplines})


# @login_required
# def group_detail(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     return render(request, 'grade_system/group_detail.html', {'group': group})


def get_groups_for_discipline(discipline):
    return Group.objects.filter(speciality__speciality_discipline__discipline=discipline).distinct()


@login_required
def teacher_dashboard(request):
    discipline_ids = request.session.get('disciplines', [])
    disciplines = Discipline.objects.filter(id__in=discipline_ids)

    disciplines_with_groups = []
    for discipline in disciplines:
        groups = get_groups_for_discipline(discipline)
        disciplines_with_groups.append({
            'discipline': discipline,
            'groups': groups
        })

    return render(request, 'grade_system/teacher_dashboard.html', {'disciplines_with_groups': disciplines_with_groups})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    discipline_id = request.GET.get('discipline_id')
    discipline = get_object_or_404(Discipline, pk=discipline_id)

    if request.method == 'POST':
        for student in Student.objects.filter(group=group):
            grade_value = request.POST.get(f'grade_{student.id}')
            if grade_value:
                grade_value = int(grade_value)
                grade, created = Grade.objects.update_or_create(
                    student=student,
                    teacher_discipline__speciality_discipline__discipline=discipline,
                    defaults={'score': grade_value}
                )
        messages.success(request, 'Оценки успешно обновлены!')
        # return redirect('grade_system:group_detail', pk=pk)

    students = Student.objects.filter(group=group).prefetch_related(
        Prefetch('grade_set', queryset=Grade.objects.filter(teacher_discipline__speciality_discipline__discipline=discipline))
    )

    student_grades = []
    for student in students:
        grade = student.grade_set.filter(teacher_discipline__speciality_discipline__discipline=discipline).first()
        student_grades.append({
            'student': student,
            'grade': grade
        })

    return render(request, 'grade_system/group_detail.html', {
        'group': group,
        'discipline': discipline,
        'students': student_grades
    })


def main_page(request):
    return render(request, 'grade_system/main.html')


def technologies_stack(request):
    return render(request, 'grade_system/technologies_stack.html')
