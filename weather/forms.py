from django.forms import ModelForm, TextInput   # text input beacuse we are adding from textbox
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}  
        #widgets is used because the 'TextInput' not showin g proper format