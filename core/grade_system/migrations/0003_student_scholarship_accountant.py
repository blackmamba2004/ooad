# Generated by Django 4.0.4 on 2024-06-04 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grade_system', '0002_student_scholarship_coefficient'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='scholarship',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Accountant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'accountant',
            },
        ),
    ]
