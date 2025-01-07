# Generated by Django 5.1.4 on 2025-01-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='llm',
            name='session',
        ),
        migrations.AddField(
            model_name='session',
            name='llm',
            field=models.ManyToManyField(to='API.llm'),
        ),
    ]
