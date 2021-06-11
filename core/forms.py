from core.models import Profile
from django.forms import ModelForm

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        exclude=['uuid']