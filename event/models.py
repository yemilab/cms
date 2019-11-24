from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class StandardEventPage(Page):
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
    body = RichTextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_allday = models.BooleanField()
    location = models.CharField(max_length=250)
    related_link = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('cover_image'),
        FieldPanel('body'),
        FieldPanel('start'),
        FieldPanel('end'),
        FieldPanel('is_allday'),
        FieldPanel('location'),
        FieldPanel('related_link')
    ]

    parent_page_types = ['EventsIndexPage']
    subpage_types = []


class EventsIndexPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    subpage_types = ['StandardEventPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(EventsIndexPage, self).get_context(request)
        context['events'] = StandardEventPage.objects.descendant_of(self).live().order_by('-start')
        return context


class SeminarPage(Page):
    date = models.DateTimeField()
    speaker = models.CharField(max_length=250)
    speaker_affiliation = models.CharField(max_length=250, blank=True)
    place = models.CharField(max_length=250)
    abstract = RichTextField()
    extra = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('speaker'),
        FieldPanel('speaker_affiliation'),
        FieldPanel('place'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('extra', classname="full"),
    ]

    parent_page_types = ['SeminarsIndexPage']
    subpage_types = []


class SeminarsIndexPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    subpage_types = ['SeminarPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(SeminarsIndexPage, self).get_context(request)
        context['posts'] = SeminarPage.objects.descendant_of(self).live().order_by('-date')
        return context
