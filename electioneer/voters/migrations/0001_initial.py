# Generated by Django 5.0.6 on 2024-06-06 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('election_name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField()),
                ('year_of_study', models.IntegerField()),
                ('faculty', models.CharField(max_length=100)),
                ('is_eligible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VotingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voters.election')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voters.student')),
            ],
        ),
    ]
