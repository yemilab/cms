from datetime import date

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from .blocks import BaseStreamBlock

@register_snippet
class Person(ClusterableModel):
    first_name = models.CharField("First name", max_length=254, help_text="First name (Latin)")
    last_name = models.CharField("Last name", max_length=254, help_text="Last name (Latin)")
    name = models.CharField("Name", max_length=254, help_text="Name (Original)", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    affiliation = models.CharField("Affiliation", max_length=254, blank=True, null=True)
    information = RichTextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name (Latin)"),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('affiliation'),
        FieldPanel('information'),
        FieldPanel('email'),
        FieldPanel('homepage'),
        ImageChooserPanel('photo'),
    ]

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class PersonPeopleIndexRelationship(Orderable, models.Model):
    page = ParentalKey(
        'PeopleIndexPage', related_name='peopleindex_person_relationship', on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'Person', related_name='person_peopleindex_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('person')
    ]


class PeopleIndexPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel(
            'peopleindex_person_relationship', label="Members(s)",
            panels=None, min_num=1),
    ]

    def members(self):
        return [ n.person for n in self.peopleindex_person_relationship.all() ]


class FaqPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True, null=True
    )
    date_published = models.DateField(
        "Date article published", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
    ]

    parent_page_types = ['FaqIndexPage',]
    subpage_types = [ ]


class FaqIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(FaqIndexPage, self).get_context(request)
        context['posts'] = FaqPage.objects.descendant_of(self).live()
        return context

    subpage_types = ['FaqPage', ]


class StandardPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body'),
    ]


class SectionPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(
        BaseStreamBlock(), verbose_name="Content block", blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body'),
    ]


@register_snippet
class HomeSlider(ClusterableModel):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    description = models.CharField(max_length=1024, null=True, blank=True)
    date_published = models.DateField("Published date")
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    related_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('description'),
        ImageChooserPanel('cover'),
        PageChooserPanel('related_page'),
        FieldPanel('date_published'),
    ]

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Home slider'
        verbose_name_plural = 'Home sliders'


class HomeHomeSliderRelationship(Orderable, models.Model):
    page = ParentalKey(
        'HomePage', related_name='home_homeslider_relationship', on_delete=models.CASCADE
    )
    homeslider = models.ForeignKey(
        'HomeSlider', related_name='homeslider_home_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('homeslider')
    ]


class HomePage(Page):
    content_panels = Page.content_panels + [
        InlinePanel(
            'home_homeslider_relationship', label="Slider(s)",
            panels=None, min_num=1),
    ]

    subpage_types = ['SectionPage', ]

    def sliders(self):
        sliders = [
            n.homeslider for n in self.home_homeslider_relationship.all()
        ]
        return sliders

    def news(self):
        return ['', '', '']

    def publications(self):
        return ['', '', '']


class GalleryPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, null=True
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )
    date_published = models.DateField("Published date")

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
        FieldPanel('collection'),
        FieldPanel('date_published'),
    ]

    parent_page_types = ['GalleriesIndexPage',]
    subpage_types = []


class GalleriesIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('image'),
    ]

    subpage_types = ['GalleryPage']

    def get_context(self, request):
        context = super(GalleriesIndexPage, self).get_context(request)
        context['galleries'] = GalleryPage.objects.descendant_of(self).live().order_by('-date_published')
        return context


class CareerPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = RichTextField()
    date_published = models.DateField("Published date")
    date_expired = models.DateField("Expired date")

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('body', classname='full'),
        FieldPanel('date_published'),
        FieldPanel('date_expired')
    ]

    parent_page_types = ['CareersIndexPage',]
    subpage_types = []

    def is_expired(self):
        return date.today() > self.date_expired


class CareersIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

    subpage_types = ['CareerPage']

    def get_context(self, request):
        context = super(CareersIndexPage, self).get_context(request)
        context['careers'] = CareerPage.objects.descendant_of(self).live().order_by('-date_expired')
        return context
