# Generated by Django 2.2 on 2020-02-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0006_candidate_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='source',
            field=models.TextField(null=True),
        ),
    ]