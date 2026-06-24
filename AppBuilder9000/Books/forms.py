from django.forms import ModelForm
from .models import Bookshelf, Book


# Creates Bookshelf Form based on Bookshelf Model
class BookshelfForm(ModelForm):
    class Meta:
        model = Bookshelf
        fields = '__all__'


# Creates Book Form based on Book Model
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
