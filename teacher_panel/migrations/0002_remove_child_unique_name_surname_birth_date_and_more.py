# Generated by Django 5.0.6 on 2024-12-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='child',
            name='unique_name_surname_birth_date',
        ),
        migrations.AddConstraint(
            model_name='child',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name', 'birth_date', 'classroom'), name='unique_name_surname_birth_date'),
        ),
    ]
