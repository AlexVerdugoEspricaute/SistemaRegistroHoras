from django import forms
from django.contrib.auth.forms import UserCreationForm                               
from .models import *


# Diccionario que mapea nombres de meses en inglés a español de los excels en la vista. 
meses_en_espanol = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

# Formulario para iniciar sesión
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'placeholder', 'placeholder': 'Ingrese su correo'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'placeholder','placeholder': 'Ingrese su contraseña'}))


# Formulario para el registro de usuarios
class AkzUsuerRegistrationForm(UserCreationForm):
    nombre = forms.CharField(label='Ingrese su Nombre', widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Ingrese su nombre'}))
    apellido = forms.CharField(label='Ingrese su Apellido', widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Ingrese su apellido'}))
    username = forms.CharField(label='Ingresa el correo', widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Ingrese su correo electrónico'}))
    email = forms.EmailField(label='Repita tu Correo electrónico', widget=forms.EmailInput(attrs={'class': '', 'placeholder': 'Repita su correo electrónico'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'placeholder', 'placeholder': 'Ingrese su contraseña'}))
    password2 = forms.CharField(label='Repita la Contraseña', widget=forms.PasswordInput(attrs={'class': 'placeholder', 'placeholder': 'Repita su contraseña'}))
    
    class Meta:
        model = AkzUsuer
        fields = ['nombre','apellido','username', 'email', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd['password2']



# Formulario para el registro de horas normales y extras
class RegistroHorasForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=PersonalEmpresa.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}), label="Persona")
    id_hito = forms.ModelChoiceField(queryset=Hito.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}), label="Hito")
    actividad = forms.ModelChoiceField(queryset=Actividad.objects.all(),widget=forms.Select(attrs={'class': 'custom-select'}), label="Actividad")
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'fecha-input'}), label="Fecha")
    horas_normales = forms.DecimalField(max_digits=5, decimal_places=0, widget=forms.NumberInput(attrs={'class': 'horas-input'}), label="Hrs Normales")
    horas_extras = forms.DecimalField(max_digits=5, decimal_places=0, required=False, widget=forms.NumberInput(attrs={'class': 'horas-input'}), label="Hrs Extras")
    observaciones = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'custom-select'}))
    seleccionar = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        jefatura_usuario = kwargs.pop('jefatura', None)
        super().__init__(*args, **kwargs)
        if user and user.usuario_administrador:
            # Si el usuario es un administrador, mostrar todas las personas bajo su jefatura
            if jefatura_usuario:
                self.fields['persona'].queryset = PersonalEmpresa.objects.filter(jefatura=jefatura_usuario)
        elif user:
            # Si el usuario no es un administrador, filtrar personas por ingreso_hora
            self.fields['persona'].queryset = PersonalEmpresa.objects.filter(ingreso_hora=user)

    #Limitador mínimo y máximo para las horas de ingreso en el formulario.  
    def clean(self):
        cleaned_data = super().clean()
        horas_fields = ['horas_normales', 'horas_extras']
        for field in horas_fields:
            horas_value = cleaned_data.get(field)
            if horas_value is not None:
                if horas_value < 0 or horas_value > 9:
                    self.add_error(field, 'El valor debe estar entre 0 y 9.')
        return cleaned_data

    class Meta:
        model = RegistroHH 
        fields = ['persona', 'id_hito','actividad' ,'fecha', 'horas_normales', 'horas_extras', 'observaciones', 'seleccionar']


# Formulario para el registro de horas vacaciones, licencias o permisos
class RegistroHorasEspecialesForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=PersonalEmpresa.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'fecha-input'}))
    fecha_termino = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'fecha-input'}))
    horas_vacaciones = forms.DecimalField(max_digits=5, decimal_places=0, required=False, widget=forms.NumberInput(attrs={'class': 'horas-input'}))
    horas_licencia = forms.DecimalField(max_digits=5, decimal_places=0, required=False, widget=forms.NumberInput(attrs={'class': 'horas-input'}))
    horas_permiso = forms.DecimalField(max_digits=5, decimal_places=0, required=False, widget=forms.NumberInput(attrs={'class': 'horas-input'}))
    observaciones = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'custom-select'}))
    actividad = forms.ModelChoiceField(queryset=Actividad.objects.all(), required=False)  # Hacer el campo actividad opcional

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        jefatura_usuario = kwargs.pop('jefatura', None)
        super().__init__(*args, **kwargs)
        if user and user.usuario_administrador:
            # Si el usuario es un administrador, mostrar todas las personas bajo su jefatura
            if jefatura_usuario:
                self.fields['persona'].queryset = PersonalEmpresa.objects.filter(jefatura=jefatura_usuario)
        elif user:
            # Si el usuario no es un administrador, filtrar personas por ingreso_hora
            self.fields['persona'].queryset = PersonalEmpresa.objects.filter(ingreso_hora=user)
    
    # Limitador mínimo para las horas de ingreso en el formulario.
    def clean(self):
        cleaned_data = super().clean()
        horas_fields = ['horas_vacaciones', 'horas_licencia', 'horas_permiso']
        for field in horas_fields:
            horas_value = cleaned_data.get(field)
            if horas_value is not None:
                if horas_value < 0 :
                    self.add_error(field, 'El valor debe ser mínimo 0.')
        return cleaned_data
    
    class Meta:
        model = RegistroHH
        fields = ['persona', 'fecha_inicio', 'actividad', 'fecha_termino', 'horas_vacaciones', 'horas_licencia', 'horas_permiso', 'observaciones']
