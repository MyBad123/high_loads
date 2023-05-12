from django.db.models import Model
from django import forms

from app.models import Book


class ModernCharField(forms.CharField):
    def __init__(self, label, name, max_length=None, min_length=None, strip=True, empty_value="", **kwargs):
        self.__label = label
        self.__name = name
        super().__init__(max_length=None, min_length=None, strip=True, empty_value="", **kwargs)

    def get_name(self):
        return self.__name

    def get_label(self):
        return self.__label



class BookForm(forms.Form):
    surname = ModernCharField(label='Фамилия автора', name='surname')
    initials = ModernCharField(label='Инициалы автора', name='initials')
    title = ModernCharField(label='Название книги', name='title')
    place = ModernCharField(label='Место издания', name='place')
    publishing = ModernCharField(label='Издательство', name='publishing')
    year = ModernCharField(label='Год издания книги', name='year')
    pages = ModernCharField(label='Количество страниц', name='pages')
    
    def get_fields(self):
        """get all fields for HTML"""

        fields = []
        
        for i in self.fields.keys():
            fields.append({
                'name': self.fields.get(i).get_name(),
                'label': self.fields.get(i).get_label(),
                'error': False,
                'is_valid': False,
                'is_valid_value': None
            })

        return fields
    
    def get_fields_with_errors(self):
        """get all fields with error"""

        list_errors = self.errors.keys()
        
        fields = []
        for i in self.get_fields():
            # set error
            if i.get('name') in list_errors:
                error = True
                is_valid = False
                value = None
            else:
                error = False
                is_valid = True
                value = self.data.get(i.get('name'))

            fields.append({
                'name': i.get('name'),
                'label': i.get('label'),
                'error': error,
                'is_valid': is_valid,
                'is_valid_value': value
            })
        
        return fields
            

    def save(self, model: Model):
        """save valid data to db"""

        if self.errors:
            raise ValueError()
        
        save_obj = model(**self.data)
        save_obj.save()
        

AllForms = {
    'book': {
        'form': BookForm,
        'model': Book
    }
}
    