# Generated by Django 2.2 on 2019-10-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0003_auto_20191029_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='party',
        ),
        migrations.AddField(
            model_name='candidate',
            name='party_number',
            field=models.TextField(null=True),
        ),
    ]