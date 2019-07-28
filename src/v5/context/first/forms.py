from django import forms

from . import models


class TemporalInputForm(forms.ModelForm):

    class Meta:
        model = models.TemporalInput
        fields = '__all__'
