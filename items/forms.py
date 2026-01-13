# items/forms.py
from django import forms
from .models import Item

class ItemReportForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'status', 'location', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe unique marks...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Blue iPhone 13'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Central Park Mall'}),
        }