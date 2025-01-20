from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'id': 'username',
            }
        ),
        label='Username',
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'id': 'password',
            }
        ),
        label='Password',
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'remember',
            }
        ),
        label='Remember me',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form labels
        for field in self.fields.values():
            if field.label != 'Remember me':  # Skip remember me checkbox
                field.label_attrs = {'class': 'form-label'}