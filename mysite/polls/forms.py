from django import forms
from .models import Stock

class StockReportForm(forms.Form):
    start_price = forms.DecimalField(required=False, min_value=0)
    end_price = forms.DecimalField(required=False, min_value=0)
    stock_type = forms.ChoiceField(choices=Stock.STOCK_TYPE_CHOICES, required=False)
