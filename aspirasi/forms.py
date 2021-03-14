from django import forms
from .models import *


class AddAspirationsForm(forms.ModelForm):
    class Meta:
        model = Aspiration
        fields = ('title', 'jenis_aspirasi', 'lokasi', 'aspirasi')


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'alamat', )
