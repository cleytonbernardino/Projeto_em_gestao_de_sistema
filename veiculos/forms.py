from django import forms


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
    cor = forms.CharField(
        label='Cor',
        widget=forms.TextInput()
    )

    placa = forms.CharField(
        label='Número da placa',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    pais = forms.CharField(
        label='Pais',
        widget=forms.TextInput()
    )
    foto_veiculo = forms.ImageField(
        label='Foto do Veículo',
    )
