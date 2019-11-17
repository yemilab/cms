from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
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

class PresentationPage(Page):
    date = models.DateField("Presentation data")
    abstract = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        InlinePanel(
            'presentation_person_relationship', label="Presentor(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
        FieldPanel('abstract', classname="full")
    ]
