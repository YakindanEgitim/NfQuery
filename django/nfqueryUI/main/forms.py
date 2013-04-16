from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        data = self.cleaned_data
        
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('Username can not be empty!'))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(_('User does not exist.'))

        return self.cleaned_data
