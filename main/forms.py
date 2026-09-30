from django.forms import ModelForm, TextInput, NumberInput, URLInput, Select
from django.forms.widgets import Textarea

from main.models import Work, Experience

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class WorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ["category", "title", "year", "photo_bw", "photo_color"]

        labels = {
            "category": "Kategori",
            "title": "Nama Project",
            "year": "Tahun",
            "photo_bw": "URL Foto (Black & White)",
            "photo_color": "URL Foto (Berwarna)",
        }

        widgets = {
            "category": Select(),
            "title": TextInput(attrs={
                "placeholder": "title",
                "maxlength": 255,
            }),
            "year": NumberInput(attrs={
                "placeholder": "tahun",
                "min": 2000,
                "max": 2100,
            }),
            "photo_bw": URLInput(attrs={
                "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
            }),
            "photo_color": URLInput(attrs={
                "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
            }),
        }

        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
            return title

        def clean_tech_stack(self):
            return strip_tags(self.cleaned_data["tech_stack"]).strip()

        def clean_description(self):
            return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "organization", "period", "description", "category"]

        labels = {
            "title": "Judul",
            "organization": "Organisasi",
            "period": "Periode",
            "description": "Deskripsi",
            "category": "Kategori",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Asisten Dosen Kalkulus 1",
                "maxlength": 255,
            }),
            "organization": TextInput(attrs={
                "placeholder": "Fakultas Ilmu Komputer UI",
                "maxlength": 255,
            }),
            "period": TextInput(attrs={
                "placeholder": "Jan 2025 - Sekarang",
                "maxlength": 100,
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan pengalamanmu",
                "rows": 4,
            }),
            "category": Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = None