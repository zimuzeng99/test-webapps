# Generated by Django 2.2.1 on 2019-05-30 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20190530_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(),
        ),
    ]