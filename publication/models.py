from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_snippet
class Journal(models.Model):
    title = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Journals"


class PresentationPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        'PresentationPage', related_name='presentation_person_relationship', on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'home.Person', related_name='person_presentation_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('person')
    ]


class PresentationPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PresentationPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PresentationPage(Page):
    date = models.DateField("Presentation date")
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)
    meeting = models.CharField(max_length=512)
    country = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)

    content_panels = Page.content_panels + [
        InlinePanel(
            'presentation_person_relationship', label="Presentor(s)",
            panels=None, min_num=1),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('meeting', classname="col6"),
                FieldPanel('country', classname="col3"),
                FieldPanel('location', classname="col3"),
            ]),
        ], "Meeting information"),
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['PresentationsIndexPage', ]


class PresentationsIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

    subpage_types = ['PresentationPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_presentations(self):
        return PresentationPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_presentations(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(PresentationsIndexPage, self).get_context(request)
        presentations = self.paginate(request, self.get_presentations())
        context['presentations'] = presentations
        return context


class PaperPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PaperPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PaperPage(Page):
    date = models.DateField("Published date")
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=PaperPageTag, blank=True)
    authors = models.TextField()
    journal = models.ForeignKey(
        'publication.Journal',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    refinfo = models.CharField("Volume, Issue, Page", max_length=250, blank=True, null=True)
    doi = models.CharField(max_length=250, blank=True, null=True)
    permalink = models.URLField("Permanent link", blank=True, null=True)
    bibtex = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('authors'),
        FieldPanel('journal'),
        FieldPanel('refinfo'),
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('doi'),
        FieldPanel('permalink'),
        FieldPanel('bibtex'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['PapersIndexPage', ]


class PapersIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

    subpage_types = ['PaperPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_papers(self):
        return PaperPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_papers(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(PapersIndexPage, self).get_context(request)
        papers = self.paginate(request, self.get_papers())
        context['papers'] = papers
        return context


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ThesisPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ThesisPage(Page):
    date = models.DateField("Published date")
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)
    author = models.ForeignKey(
        'home.Person', related_name='+', on_delete=models.PROTECT
    )
    publisher = models.CharField(max_length=250)
    advisor = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        SnippetChooserPanel('author'),
        FieldPanel('publisher'),
        FieldPanel('advisor'),
        FieldPanel('date'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('tags'),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['ThesesIndexPage', ]


class ThesesIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

    subpage_types = ['ThesisPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_theses(self):
        return ThesisPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_theses(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(ThesesIndexPage, self).get_context(request)
        theses = self.paginate(request, self.get_theses())
        context['theses'] = theses
        return context
