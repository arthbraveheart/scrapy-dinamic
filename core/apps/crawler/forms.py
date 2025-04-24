from django import forms

from target.models import Curva


class SellerForm(forms.Form):
    MAKE_MAP = [
        ('mercado_livre', "Mercado Livre"),
        ("carrefas", "Carrefour"),
        ("madeira", "Madeira Madeira"),
        ("magalu","Magazine Luiza"),
        #("testing", "testing"),
    ]

    SPIDERS_MAP = [
        ('ml_curva', "Mercado Livre"),
        ("carrefas_curva", "Carrefour"),
        ("madeira_curva", "Madeira Madeira"),
        ("magalu_curva", "Magazine Luiza"),
        # ("testing", "testing"),
    ]

    seller = forms.ChoiceField(
        label="Escolha um concorrente para buscar os preços:",
        choices=SPIDERS_MAP,#MAKE_MAP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        )

    curva = forms.ModelChoiceField(
        queryset=Curva.objects.all(),#.values_list('name', flat=True),
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

