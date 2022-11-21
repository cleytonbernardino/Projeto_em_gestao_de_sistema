from django import forms


class UserLoginForm(forms.Form):

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu email',
            'autocomplete': 'off',
        }),
        error_messages={
            'required': 'Por favor insira sua email',
        }
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        }),
        error_messages={
            'required': 'Por favor insira sua senha',
        }
    )

    lembre_me = forms.CharField(
        required=False,
        label='Lembre-me',
        widget=forms.CheckboxInput(attrs={
            'style': 'height: 1rem; width: 1rem;'
        })
    )
