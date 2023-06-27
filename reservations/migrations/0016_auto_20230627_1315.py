# Generated by Django 3.2.19 on 2023-06-27 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0015_auto_20230626_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.menu'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
