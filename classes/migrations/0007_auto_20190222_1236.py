# Generated by Django 2.1.5 on 2019-02-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_auto_20190222_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=6),
        ),
    ]
