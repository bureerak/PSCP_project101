# Generated by Django 5.1.1 on 2024-11-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_room_last_joined_room_turn_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_turn',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='turn_list',
            field=models.JSONField(default=['Waiting']),
        ),
    ]
