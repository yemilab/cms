from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from .models import Person, HomeSlider
from publication.models import Journal
from blog.models import TweetPage

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''


class PeopleModelAdmin(ModelAdmin):
    model = Person
    menu_label = 'People'
    menu_icon = 'fa-users'
    list_display = ('last_name', 'first_name', 'name', 'affiliation', 'email', 'phone')
    ordering = ('name', 'last_name', 'first_name')


class JournalModelAdmin(ModelAdmin):
    model = Journal
    menu_label = 'Journal'
    menu_icon = 'fa-book'
    list_display = ('title', 'abbreviation')
    ordering = ('title', )

class HomeSliderModelAdmin(ModelAdmin):
    model = HomeSlider
    menu_label = 'Home sliders'
    menu_icon = 'fa-bullhorn'
    list_display = ('title', 'subtitle', 'description', 'date_published')
    ordering = ('-date_published', )

class TweetPageModelAdmin(ModelAdmin):
    model = TweetPage
    menu_label = 'Physics News'
    menu_icon = 'fa-twitter'
    list_display = ('title', 'date_published')
    ordering = ('-date_published', )

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(PeopleModelAdmin)
modeladmin_register(JournalModelAdmin)
modeladmin_register(HomeSliderModelAdmin)
modeladmin_register(TweetPageModelAdmin)
