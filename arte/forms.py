from django import forms
from .models.comentario import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('usuario', 'comentario',)