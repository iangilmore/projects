# Generated by Django 5.0.6 on 2024-05-14 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_project_delete_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='url',
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Live Demo', 'Live Demo'), ('Deployment', 'Deployment'), ('Source Repository', 'Source Repository'), ('Frontend Source Repository', 'Frontend Source Repository'), ('Backend Source Repository', 'Backend Source Repository'), ('Wireframes', 'Wireframes'), ('ERD', 'ERD'), ('Component Hierachy Diagram', 'Component Hierachy Diagram'), ('Custom', 'Custom')])),
                ('custom_type', models.CharField(blank=True, max_length=50)),
                ('url', models.URLField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.project')),
            ],
        ),
    ]
