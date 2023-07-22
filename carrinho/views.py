from typing import Any, Dict
from django import http
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models.carrinho import Carrinho
from arte.models.arte import Arte
from django.shortcuts import redirect, get_object_or_404 
from django.urls import  reverse, reverse_lazy
from arte.views import ComentarioDelete

# Create your views here.
class AdicionarArteCarrinho(View):
    
    def get(self, request, pk):
        arte = get_object_or_404(Arte, id=pk)
        return render(request, 'carrinho/adicionar_arte_carrinho.html', context={'arte':arte})
    
    def post(self, request, pk):
        usuario = request.user
        arte = get_object_or_404(Arte, id=pk)
        arte_salvo = usuario in arte.salvo.all()
              
        if arte_salvo:
            return redirect(reverse('arte_lista'))
        else:
            arte.salvo.add(usuario)
            Carrinho(usuario=self.request.user, arte=arte).save()
            return redirect(reverse('carrinho_lista'))
           
class CarrinhoItens(TemplateView):
    template_name = 'carrinho_itens.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens'] = Carrinho.objects.filter(usuario=self.request.user)
        context['quantidade'] = Carrinho.quantidade
        context['preco_total'] = Carrinho.preco_total(self.request)
        return context
    
class DeletarArteCarrinho(ComentarioDelete):
    
    def get_success_url(self):
        return reverse('carrinho_lista')
    
    def get(self, request, pk):
        carrinho_arte = get_object_or_404(Carrinho, id=pk)
        return render(request, 'carrinho/carrinho_delete.html', context={'carrinho_arte':carrinho_arte})
    
    def post(self, request, pk):
        carrinho_arte = get_object_or_404(Carrinho, id=pk)
        carrinho_arte.arte.salvo.remove(request.user)
        Carrinho.objects.get(id=pk).delete()
        return redirect(reverse('carrinho_lista'))