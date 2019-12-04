from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_snippet
class Meeting(models.Model):
    name = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    start_date = models.DateField("Start date")
    end_date = models.DateField("End date")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Meetings"


@register_snippet
class Journal(models.Model):
    title = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=100, blank=True)
    doi = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Journals"


@register_snippet
class Collaboration(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Collaborations"


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
    abstract = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)
    meeting = models.ForeignKey(
        'publication.Meeting',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    collaboration = models.ForeignKey(
        'publication.Collaboration',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('meeting'),
        FieldPanel('date'),
        InlinePanel(
            'presentation_person_relationship', label="Presentor(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
        FieldPanel('abstract', classname="full")
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


class PaperPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        'PaperPage', related_name='paper_person_relationship', on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'home.Person', related_name='person_paper_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('person')
    ]


class PaperPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PaperPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PaperPage(Page):
    authors = models.CharField(max_length=10240, blank=True)
    collaboration = models.ForeignKey(
        'publication.Collaboration',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    date = models.DateField("Published date")
    journal = models.ForeignKey(
        'publication.Journal',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    page = models.CharField(max_length=100, blank=True)
    volume = models.CharField(max_length=100, blank=True)
    issue = models.CharField(max_length=100, blank=True)
    abstract = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('authors'),
        FieldPanel('collaboration'),
        InlinePanel(
            'paper_person_relationship', label="Corresponding author(s)",
            panels=None, min_num=1),
        FieldPanel('date'),
        MultiFieldPanel([
            FieldPanel('journal'),
            FieldPanel('page'),
            FieldPanel('volume'),
            FieldPanel('issue'),
        ], heading="Journal section"),
        FieldPanel('tags'),
        FieldPanel('abstract', classname="full")
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


class ThesisPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        'ThesisPage', related_name='thesis_person_relationship', on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'home.Person', related_name='person_thesis_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('author')
    ]


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ThesisPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ThesisPage(Page):
    author = models.ForeignKey(
        'home.Person', related_name='+', on_delete=models.PROTECT
    )
    publisher = models.CharField(max_length=250)
    advisor = models.CharField(max_length=250, blank=True)
    date = models.DateField("Published date")
    abstract = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)

    content_panels = Page.content_panels + [
        SnippetChooserPanel('author'),
        FieldPanel('publisher'),
        FieldPanel('advisor'),
        FieldPanel('date'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('tags'),
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
