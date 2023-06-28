from django.db import models
from .arte import Arte

class Comentario(models.Model):
    usuario = models.CharField(max_length=15)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField(max_length=300)
    criado_em = models.TimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criado_em']
        
    def __str__(self) -> str:
        return 'comentario {} por {}'.format(self.arte, self.usuario)