from django.db import models
from django.db.models import OneToOneField
from django.conf import settings


class Accountant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'accountant'

    def __str__(self):
        return f'{self.full_name}'


class Teacher(models.Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return f'{self.full_name}'


class Speciality(models.Model):

    class Status(models.TextChoices):
        PR = 'ПР', 'Программная инженерия'
        PI = 'ПИ', 'Прикладная информатика'
        IV = 'ИВ', 'Информатика и вычислительная техника'
        IB = 'ИБ', 'Информационная безопасность'
        US = 'УС', 'Управление в технических системах'
        KB = 'КБ', 'Компьютерная безопасность'
        AS = 'АС', 'Безопасность автоматизированных систем'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2, choices=Status.choices)
    code = models.CharField(max_length=10)
    year = models.PositiveIntegerField()

    class Meta:
        db_table = 'speciality'
        unique_together = ['name', 'year']

    def __str__(self):
        return f'{self.name}, {self.year}'


class Discipline(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    is_credit = models.BooleanField(default=False)

    class Meta:
        db_table = 'discipline'

    def __str__(self):
        return f'{self.title}'


class Group(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField(default=1)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.name


class Student(models.Model):

    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    scholarship_coefficient = models.FloatField(default=1.0)
    scholarship = models.FloatField(default=0.0)

    class Meta:
        db_table = 'student'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()
        super().save(*args, **kwargs)

    def generate_id(self):
        last_student = Student.objects.filter(group=self.group).order_by('-id').first()

        if last_student:
            last_id = int(last_student.id.split('-')[-1])
            new_id = last_id + 1
        else:
            new_id = 1

        return f'{self.group}-{new_id}'

    def __str__(self):
        return f'{self.id}, {self.name}'


class Speciality_Discipline(models.Model):

    id = models.AutoField(primary_key=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    class Meta:
        db_table = 'speciality_discipline'

    def __str__(self):
        return f'{self.discipline}, {self.speciality}'


class Teacher_Discipline(models.Model):

    id = models.AutoField(primary_key=True)
    speciality_discipline = models.ForeignKey(Speciality_Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher_discipline'

    def __str__(self):
        return f'{self.speciality_discipline}'


class Grade(models.Model):

    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_discipline = models.ForeignKey(Teacher_Discipline, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'grade'

    def is_passed(self):
        return self.score == 5

    def __str__(self):
        return f'{self.score}'


