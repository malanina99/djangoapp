# Generated by Django 3.0.7 on 2020-06-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='is_mvp',
            field=models.BooleanField(default=False),
        ),
    ]