from django.utils import translation

class TranslatedField:
    def __init__(self, en_field, ko_field):
        self.en_field = en_field
        self.ko_field = ko_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'ko':
            return getattr(instance, self.ko_field)
        else:
            return getattr(instance, self.en_field)
