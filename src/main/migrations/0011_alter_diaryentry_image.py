# Generated by Django 4.1.4 on 2022-12-19 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_diaryentry_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diaryentry',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
