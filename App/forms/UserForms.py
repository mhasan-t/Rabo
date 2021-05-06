from django import forms


class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'enter your first name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'enter your last name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'enter your e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'enter your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'enter your password again'}))

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class LoginUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'enter your e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'enter your password'}))
