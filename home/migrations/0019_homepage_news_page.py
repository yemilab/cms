# Generated by Django 2.2.7 on 2019-12-10 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0018_auto_20191210_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='news_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
    ]
