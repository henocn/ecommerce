from django import forms
from compte.models import Client

class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["username", "last_name", "email", "password", "profil", "pays"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        for element in self.fields:
            self.fields[element].widget.attrs.update({
                'class': 'form-control form-control-sm mb-3'
            })

