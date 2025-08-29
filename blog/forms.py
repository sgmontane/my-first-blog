from django import forms
from .models import BuildRecord, Builder, SubAssembly

class BuildRecordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = BuildRecord
        fields = ['builder', 'subassembly', 'time_minutes', 'build_date', 'password']
        labels = {
            'builder': 'Builder Name',
            'subassembly': 'Sub Assembly',
            'time_minutes': 'Time (minutes)',
            'build_date': 'Date Built',
        }

        widgets = {
            'build_date': forms.DateInput(attrs={'type': 'date'}),
        }
