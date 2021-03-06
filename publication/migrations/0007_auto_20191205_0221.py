# Generated by Django 2.2.7 on 2019-12-05 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0006_auto_20191205_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperpage',
            name='refinfo',
            field=models.CharField(default='Unknown', max_length=250, verbose_name='Volume, Issue, Page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paperpage',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Permanent link'),
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='country',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='location',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
