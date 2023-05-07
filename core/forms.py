from django.forms import ModelForm
from .models import *

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = [ 'topic', 'name','description']

        
        