# Generated by Django 2.2 on 2020-02-23 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoobang', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoobang',
            name='source',
            field=models.TextField(null=True),
        ),
    ]