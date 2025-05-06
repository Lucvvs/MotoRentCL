from django import forms
from .models import Contacto, Reserva, UsuarioRegistro


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'correo', 'celular', 'asunto', 'mensaje']
        widgets = {
            'nombre':  forms.TextInput(attrs={'class':'form-control','placeholder':'Tu nombre completo','required':True}),
            'correo':  forms.EmailInput(attrs={'class':'form-control','placeholder':'tu@email.com','required':True}),
            'celular': forms.TextInput(attrs={'class':'form-control','placeholder':'+56 9 8765 4321','required':True}),
            'asunto':  forms.Select(attrs={'class':'form-select','required':True}),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe los detalles de tu solicitud aquí...',
                'required': True
            }),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_cliente', 'correo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }




class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False
    )

    class Meta:
        model = UsuarioRegistro
        fields = ['nombre', 'correo', 'telefono', 'nacionalidad', 'contrasena']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Deja el campo contraseña vacío, aunque el usuario tenga un valor en DB
        self.fields['contrasena'].initial = ''