# Generated by Django 3.2 on 2021-06-05 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
    ]
