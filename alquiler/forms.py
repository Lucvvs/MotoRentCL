from django import forms
from .models import Contacto, Reserva

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