from django import forms
from django.db import models


class SearchForm(forms.Form):
    instant_q = forms.CharField(widget=forms.TextInput(attrs={'id':'ajaxsearch', 'class':'search-input', 'placeholder':'Type to search',
                                'autofocus':'autofocus'}), required=False)
    people_q = forms.CharField(widget=forms.TextInput(attrs={'id':'ajaxsearch', 'class':'search-input', 'placeholder':'Name, Major, or Society',
                               'autofocus':'autofocus'}), required=False)
