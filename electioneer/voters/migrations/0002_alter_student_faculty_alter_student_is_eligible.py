# Generated by Django 5.0.6 on 2024-06-06 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='faculty',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_eligible',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3),
        ),
    ]
