from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
                    input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                    help_text='YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY'
                    )

    class Meta:
        model = Menu
        exclude = ('created_date',)
