from django import forms

class NameForm(forms.Form):

        username = forms.CharField(max_length=4)
        password = forms.CharField(max_length=8)
