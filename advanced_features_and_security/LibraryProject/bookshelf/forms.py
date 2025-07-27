from django import forms

class BookSearchForm(forms.Form):
    ExampleForm = forms.CharField(max_length=100, required=True)
