# Generated by Django 3.0.3 on 2020-02-07 06:33

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('home', '0023_peopleindexpage_view_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlumniPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_ko', models.CharField(max_length=255, verbose_name='Title (Korean)')),
                ('description', models.TextField(blank=True, help_text='Text to describe the page', verbose_name='Description (English)')),
                ('description_ko', models.TextField(blank=True, help_text='Text to describe the page', verbose_name='Description (Korean)')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='peopleindexpage',
            name='view_type',
        ),
        migrations.CreateModel(
            name='PersonAlumniRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='alumni_person_relationship', to='home.AlumniPage')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_alumni_relationship', to='home.Person')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]