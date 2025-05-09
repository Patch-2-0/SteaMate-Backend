# Generated by Django 4.2 on 2025-03-11 05:20

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_merge_20250311_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='preferred_game',
            field=models.ManyToManyField(blank=True, related_name='users_preferred_game', through='account.UserPreferredGame', to='account.game'),
        ),
        migrations.AlterField(
            model_name='user',
            name='preferred_genre',
            field=models.ManyToManyField(blank=True, related_name='users_preferred_genre', to='account.genre'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=20, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), django.core.validators.MinLengthValidator(5)], verbose_name='username'),
        ),
    ]
