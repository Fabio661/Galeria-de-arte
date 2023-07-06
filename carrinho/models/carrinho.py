from django.db import models
from django.contrib.auth.models import User
from arte.models.arte import Arte

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    
    def preco_total(request):
        preco_total = 0
        
        for item in Carrinho.objects.all():
            preco_total += item.arte.preco
        return preco_total
        