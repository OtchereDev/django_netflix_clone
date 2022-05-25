# 영상 2:07:00
from django.forms import ModelForm
from .models import Profile

class profileForm(ModelForm):
    class Meta:
        model=Profile
        exclude=['uuid']
