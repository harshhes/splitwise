# Generated by Django 5.0.1 on 2024-01-14 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_managers_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseparticipant',
            name='final_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
