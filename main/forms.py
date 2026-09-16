from django.forms import ModelForm, TextInput, NumberInput, URLInput, Select

from main.models import Work


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