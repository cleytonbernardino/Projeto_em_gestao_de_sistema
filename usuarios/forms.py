from django import forms


class UserRegisterForm(forms.Form):

    nome = forms.CharField(
        label='Nome Completo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome completo do funcionario',
            'autocomplete': 'off',
        }),
        error_messages={
            'required': 'O nome completo é obrigatorio',
        },
    )

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
