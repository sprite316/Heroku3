# Generated by Django 2.2 on 2020-03-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotlist',
            name='source',
            field=models.TextField(null=True),
        ),
    ]