from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

#class stock_price_view_search(forms):
 #   company = forms.Charfield(label='종목코드')

# form 의 select tag(dropdown list) 용도
class MyCompanyList(forms.Form):

    종목코드 = forms.ModelChoiceField(
        queryset=StockList.objects.values_list("company_id", flat=True).distinct(), empty_label=None
    )