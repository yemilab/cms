from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_snippet
class People(ClusterableModel):
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
    ]

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


@register_snippet
class HomeSlider(ClusterableModel):
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('cover'),
    ]


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

    def sliders(self):
        sliders = [
            n.homeslider for n in self.home_homeslider_relationship.all()
        ]
        return sliders

    def news(self):
        return ['', '', '']

    def publications(self):
        return ['', '', '']
