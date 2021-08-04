from django import forms
from app.models import Customer

'''We have the models in our app/models.py, so we can use it to make a form for the registration.
We just settings some specific conditions about the registration and we add "clean function"
to manage the password.
Now we can go to the acoounts/views.py to create the registration form'''


class Registration_Form(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        super().clean()
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError(" Password are different...Try again! ")
        return self.cleaned_data