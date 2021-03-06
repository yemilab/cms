# Generated by Django 2.2.7 on 2019-12-04 12:50

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20191204_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='affiliation',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Affiliation'),
        ),
        migrations.AddField(
            model_name='person',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='homepage',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='information',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(blank=True, help_text='Name (Original)', max_length=254, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(help_text='First name (Latin)', max_length=254, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(help_text='Last name (Latin)', max_length=254, verbose_name='Last name'),
        ),
    ]
