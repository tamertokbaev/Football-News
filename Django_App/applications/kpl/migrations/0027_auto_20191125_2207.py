# Generated by Django 2.2.6 on 2019-11-25 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpl', '0026_auto_20191125_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eu_cycle',
            name='group',
            field=models.CharField(default='I', max_length=1),
        ),
    ]
