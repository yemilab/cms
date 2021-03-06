from datetime import datetime

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, RichTextField, StreamFieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.api import APIField

from home.blocks import BaseStreamBlock
from home.custom_fields import TranslatedField


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
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True, null=True
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_allday = models.BooleanField()
    location = models.CharField(max_length=250)
    related_link = models.URLField(blank=True)
    abstract_deadline = models.DateTimeField(blank=True, null=True)
    our_speakers = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        FieldPanel('start'),
        FieldPanel('end'),
        FieldPanel('is_allday'),
        FieldPanel('location'),
        FieldPanel('related_link'),
        FieldPanel('abstract_deadline'),
        FieldPanel('our_speakers'),
    ]

    parent_page_types = ['EventsIndexPage']
    subpage_types = []

    api_fields = [
        APIField('start'),
        APIField('end'),
        APIField('is_allday'),
        APIField('location'),
        APIField('related_link'),
    ]


class EventsIndexPage(Page):
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
    view_type = models.CharField(max_length=64, choices=[('list', 'List'), ('table', 'Table')], default='list')

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
        FieldPanel('view_type'),
    ]

    subpage_types = ['StandardEventPage']

    def get_context(self, request):
        context = super(EventsIndexPage, self).get_context(request)
        events = StandardEventPage.objects.live().descendant_of(self)
        year = None
        if request.GET.get('year') == 'all':
            pass
        elif not request.GET.get('year') in [None, '']:
            try:
                year = int(request.GET.get('year'))
                events = events.filter(start__year=year)
            except ValueError:
                pass
        else: # if (request.GET.get('year') in [None, '']) is True, year will be this year.
            year = datetime.now().year
            events = events.filter(start__year=year)
        context['events'] = events.order_by('-start')
        context['years'] = range(datetime.now().year+1, 2012, -1)
        context['selected_year'] = year
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

    subpage_types = ['SeminarPage']

    def get_context(self, request):
        context = super(SeminarsIndexPage, self).get_context(request)
        seminars = SeminarPage.objects.live().descendant_of(self)
        year = None
        if request.GET.get('year') == 'all':
            pass
        elif not request.GET.get('year') in [None, '']:
            try:
                year = int(request.GET.get('year'))
                seminars = seminars.filter(date__year=year)
            except ValueError:
                pass
        else: # if (request.GET.get('year') in [None, '']) is True, year will be this year.
            year = datetime.now().year
            seminars = seminars.filter(date__year=year)
        context['seminars'] = seminars.order_by('-date')
        context['years'] = range(datetime.now().year, 2012, -1)
        context['selected_year'] = year
        return context
