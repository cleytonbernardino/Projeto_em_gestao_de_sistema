from django import forms


class PlacaForm(forms.Form):
    placa = forms.CharField(
        label='Placa',
        widget=forms.TextInput(attrs={
            'class': 'input-placa',
            'placeholder': 'Digite a placa sem traço',
            'autocomplete': 'off',
        }),
        error_messages={
            'required': 'Digite uma placa Primeiro'
        },
    )


class VeiculoForm(forms.Form):
    proprietario = forms.CharField(
        label='Nome do Proprietario',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    modelo = forms.CharField(
        label='Modelo do Veiculo',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    num_chassi = forms.CharField(
        label='Número do chassi',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    placa = forms.CharField(
        label='Número da placa',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    pais = forms.CharField(
        label='Pais',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    foto_veiculo = forms.ImageField(
        label='Foto do Veículo',
    )
