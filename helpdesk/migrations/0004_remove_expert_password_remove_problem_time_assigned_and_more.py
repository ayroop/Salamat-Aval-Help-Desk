# Generated by Django 4.2.7 on 2023-11-11 17:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0003_fileattachment_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='password',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='time_assigned',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='password',
        ),
        migrations.AddField(
            model_name='expert',
            name='current_assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_assignment_expert', to='helpdesk.problem'),
        ),
        migrations.AddField(
            model_name='expert',
            name='problem_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='helpdesk.problemtype'),
        ),
        migrations.AddField(
            model_name='notification',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='helpdesk.problem'),
        ),
        migrations.AddField(
            model_name='staff',
            name='current_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_request_staff', to='helpdesk.problem'),
        ),
        migrations.AlterField(
            model_name='fileattachment',
            name='file_size',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4194304)]),
        ),
        migrations.AlterField(
            model_name='fileattachment',
            name='file_type',
            field=models.CharField(choices=[('JPG', 'JPG'), ('PNG', 'PNG')], max_length=50),
        ),
        migrations.AlterField(
            model_name='notification',
            name='send_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.CharField(choices=[('staff', 'Staff'), ('admin', 'Admin')], max_length=50),
        ),
    ]
