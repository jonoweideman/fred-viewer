from django import forms

class FREDForm(forms.Form):
    series = forms.CharField(label='FRED Time Series', max_length=20)