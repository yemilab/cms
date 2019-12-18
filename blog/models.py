from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, RichTextField, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from home.blocks import BaseStreamBlock
from home.custom_fields import TranslatedField


class BlogPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'home.Person', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('person')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPage(Page):
    subtitle = models.CharField(blank=True, max_length=255)
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date_published = models.DateField(
        "Date article published", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        InlinePanel(
            'blog_person_relationship', label="Author(s)",
            panels=None),
        FieldPanel('tags'),
    ]

    def authors(self):
        return [ n.person for n in self.blog_person_relationship.all() ]

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    parent_page_types = ['BlogIndexPage']
    subpage_types = []


class BlogIndexPage(RoutablePageMixin, Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
        ImageChooserPanel('image'),
    ]

    subpage_types = ['BlogPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        return context

    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


class TweetPage(Page):
    body = RichTextField()
    date_published = models.DateField(
        "Date article published", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('date_published'),
    ]


    parent_page_types = ['TweetIndexPage']
    subpage_types = []


class TweetIndexPage(Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
    ]

    subpage_types = ['TweetPage']

    def get_context(self, request):
        context = super(TweetIndexPage, self).get_context(request)
        context['tweets'] = TweetPage.objects.descendant_of(self).live().order_by('-date_published')
        return context
