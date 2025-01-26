from django import forms
from .models import Advertisement, Category


class AdvertisementForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Advertisement
        fields = ['category', 'title', 'content', 'image', 'video_url']
