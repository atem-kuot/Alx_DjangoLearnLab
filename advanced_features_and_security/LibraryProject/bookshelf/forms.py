from django import forms

class ExampleForm(forms.Form):
    Query = forms.CharField(max_length=100, required=True)
