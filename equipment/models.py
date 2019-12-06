from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    parent_page_types = ['EquipmentIndexPage']
    subpage_types = []

    def authors(self):
        return [ n.person for n in self.equipment_photo_relationship.all() ]


class EquipmentIndexPage(Page):
    description = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

    subpage_types = ['StandardEquipmentPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_equipment(self):
        return StandardEquipmentPage.objects.live().descendant_of(self).order_by('title')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_equipment(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(EquipmentIndexPage, self).get_context(request)
        equipment = self.paginate(request, self.get_equipment())
        context['equipment'] = equipment
        return context
