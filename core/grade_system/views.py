from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Subquery, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Teacher, Discipline, Group, Student, Grade, Teacher_Discipline, Accountant


def get_teacher_disciplines(teacher):
    disciplines = Discipline.objects.filter(
        speciality_discipline__teacher_discipline__teacher=teacher
    ).distinct()
    return disciplines


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
                        request.session['disciplines'] = [discipline.id for discipline in disciplines]
                        # Перенаправление на панель преподавателя
                        return redirect('grade_system:teacher_dashboard')
                    except Teacher.DoesNotExist:
                        pass

                    # Проверка, является ли пользователь бухгалтером
                    try:
                        accountant = Accountant.objects.get(user=user)
                        # Перенаправление на панель бухгалтера
                        return redirect('grade_system:accountant_dashboard')
                    except Accountant.DoesNotExist:
                        return HttpResponse('Вы не являетесь преподавателем или бухгалтером!')
                else:
                    return HttpResponse('Ваша запись отключена!')
            else:
                return HttpResponse('Недопустим вход!')
    else:
        form = LoginForm()
    return render(request, 'grade_system/login_form.html', {'form': form})


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
def accountant_dashboard(request):
    students = Student.objects.all()  # Получение всех студентов, замените эту строку на ваш код получения студентов из базы данных
    return render(request, 'grade_system/accountant_dashboard.html', {'students': students})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    discipline_id = request.GET.get('discipline_id')
    discipline = get_object_or_404(Discipline, pk=discipline_id)

    if request.method == 'POST':
        for student in Student.objects.filter(group=group):
            if discipline.is_credit:
                is_passed = request.POST.get(f'grade_{student.id}') == 'on'
                grade_value = 5 if is_passed else None
            else:
                grade_value = request.POST.get(f'grade_{student.id}')
                if grade_value:
                    grade_value = int(grade_value)
                else:
                    grade_value = 0

            teacher_discipline = Teacher_Discipline.objects.get(
                speciality_discipline__discipline=discipline,
                speciality_discipline__speciality=group.speciality
            )
            Grade.objects.update_or_create(
                student=student,
                teacher_discipline=teacher_discipline,
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
            'grade': grade,
            'is_passed': grade.is_passed() if grade else False
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


@csrf_protect
def calculate_coefficients(request):
    if request.method == 'POST':
        students = Student.objects.all()
        for student in students:
            grades = Grade.objects.filter(student=student)
            all_grades_five = all(grade.score == 5 for grade in grades)
            has_grade_four = any(grade.score == 4 for grade in grades)
            has_grade_three = any(grade.score == 3 for grade in grades)
            if all_grades_five:
                student.scholarship_coefficient = 1.5
            elif has_grade_four and not has_grade_three:
                student.scholarship_coefficient = 1
            else:
                student.scholarship_coefficient = 0

            student.save()

    return redirect('grade_system:accountant_dashboard')


@csrf_protect
def calculate_scholarship(request):
    if request.method == 'POST':
        base_scholarship = float(request.POST.get('base_scholarship'))
        for student in Student.objects.all():
            student.scholarship = base_scholarship * student.scholarship_coefficient
            student.save()
        return redirect('grade_system:accountant_dashboard')
