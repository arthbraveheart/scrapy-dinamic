from django import forms


class SellerForm(forms.Form):
    MAKE_MAP = [
        ('mercado_livre', "Mercado Livre"),
        ("carrefas", "Carrefour"),
        ("madeira", "Madeira Madeira"),
        ("testing", "testing"),
    ]

    seller = forms.ChoiceField(
        choices=MAKE_MAP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        )