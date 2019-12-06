from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, RichTextField, StreamFieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class EquipmentPhotoRelationship(Orderable, models.Model):
    equipment = ParentalKey(
        'StandardEquipmentPage', related_name='equipment_photo_relationship', on_delete=models.CASCADE
    )
    photo = models.ForeignKey(
        'wagtailimages.Image', related_name='photo_equipment_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('photo')
    ]


class StandardEquipmentPage(Page):
    DATEFMT = [
        ('Y', 'Year'),
        ('YM', 'Year-Month'),
        ('YMD', 'Year-Month-Date'),
    ]
    cover_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    manufacturer = models.CharField(max_length=256)
    manufacture_date_fmt = models.CharField(max_length=8, choices=DATEFMT, default='YMD')
    manufacture_date = models.DateField()
    model = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    manager = models.ForeignKey(
        'home.Person',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.PROTECT
    )
    related_link = models.URLField(blank=True, null=True)
    purpose = RichTextField(blank=True, null=True)
    spec = RichTextField("Specification and performance", blank=True, null=True)
    photos = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover_photo'),
        FieldPanel('manufacturer'),
        FieldPanel('manufacture_date_fmt'),
        FieldPanel('manufacture_date'),
        FieldPanel('model'),
        FieldPanel('location'),
        FieldPanel('purpose', classname='full'),
        FieldPanel('spec', classname='full'),
        InlinePanel(
            'equipment_photo_relationship',
            label="Photo(s)",
            panels=None),
        FieldPanel('related_link'),
        FieldPanel('extra', classname='full'),
    ]

    #parent_page_types = ['EventsIndexPage']
    #subpage_types = []

    def authors(self):
        return [ n.person for n in self.equipment_photo_relationship.all() ]
