from django.db import models

class Categoria(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.titulo