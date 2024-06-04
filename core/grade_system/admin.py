from django.contrib import admin

from .models import (Teacher, Speciality, Discipline, Group, Student, Grade,
                     Teacher_Discipline, Speciality_Discipline, Accountant)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']


@admin.register(Accountant)
class AccountantAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'year']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_credit']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'semester', 'speciality']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']


@admin.register(Speciality_Discipline)
class SpecialityDisciplineAdmin(admin.ModelAdmin):
    list_display = ['id', 'semester', 'speciality', 'discipline', 'active']


@admin.register(Teacher_Discipline)
class TeacherDisciplineAdmin(admin.ModelAdmin):
    list_display = ['id', 'speciality_discipline', 'teacher']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'teacher_discipline', 'student']