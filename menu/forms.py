from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    season = forms.CharField(max_length=20, required=True)
    expiration_date = forms.DateField(
                    input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                    help_text='YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY',
                    required=True
                    )

    class Meta:
        model = Menu
        exclude = ('created_date',)
