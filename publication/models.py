from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class PresentationPeopleRelationship(Orderable, models.Model):
    page = ParentalKey(
        'PresentationPage', related_name='presentation_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'home.People', related_name='person_presentation_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class PresentationPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PresentationPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

@register_snippet
class Meeting(models.Model):
    name = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Meetings"


class PresentationPage(Page):
    date = models.DateField("Presentation data")
    abstract = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)
    meeting = models.ForeignKey(
        'publication.Meeting',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
