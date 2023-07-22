from django.db import models
from django.contrib.auth.models import User
from arte.models.categoria import Categoria

class Arte(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='image/', blank=True)
    descricao = models.CharField(max_length=200, blank=True)
    preco = models.IntegerField(null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='like_arte')
    salvo = models.ManyToManyField(User, blank=True, related_name='salvar_arte')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-criado_em']
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.titulo