# Generated by Django 2.2.7 on 2019-11-17 13:56

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('home', '0003_people'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('publication', '0007_auto_20191117_0416'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('authors', models.CharField(blank=True, max_length=10240)),
                ('date', models.DateField(verbose_name='Presentation date')),
                ('page', models.CharField(blank=True, max_length=100)),
                ('volume', models.CharField(blank=True, max_length=100)),
                ('issue', models.CharField(blank=True, max_length=100)),
                ('abstract', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlesIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Collaborations',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('abbreviation', models.CharField(blank=True, max_length=100)),
                ('doi', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Journals',
            },
        ),
        migrations.CreateModel(
            name='ArticlePeopleRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_person_relationship', to='publication.ArticlePage')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_article_relationship', to='home.People')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='publication.ArticlePage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publication_articlepagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='articlepage',
            name='collaboration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publication.Collaboration'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='journal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publication.Journal'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='publication.PresentationPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='collaboration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publication.Collaboration'),
        ),
    ]