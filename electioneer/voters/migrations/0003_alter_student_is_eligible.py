# Generated by Django 5.0.6 on 2024-06-06 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0002_alter_student_faculty_alter_student_is_eligible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='is_eligible',
            field=models.BooleanField(default=True),
        ),
    ]
