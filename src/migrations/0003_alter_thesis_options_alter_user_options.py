# Generated by Django 4.1.7 on 2023-03-28 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_user_token_count_user_token_updated_at_thesis'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thesis',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-pk']},
        ),
    ]
