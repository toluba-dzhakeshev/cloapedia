# Generated by Django 3.2.6 on 2021-08-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, choices=[('grey', 'grey'), ('red', 'red'), ('aqua', 'aqua'), ('yellow', 'yellow'), ('pink', 'pink'), ('green', 'green')], max_length=6, null=True),
        ),
    ]
