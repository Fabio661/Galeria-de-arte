from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from arte.factories import UsuarioFactory, CategoriaFactory
from arte.models.arte import Arte
from carrinho.models.carrinho import Carrinho

class CarrinhoTeste(TestCase):
    
    def setUp(self):
        
        self.usuario = UsuarioFactory(username='usuario_teste')   
        self.client.force_login(user=self.usuario)
        
        self.categoria = CategoriaFactory(titulo='classicista',
                                          slug='classicista',
                                          descricao='descricao teste')
        
        self.arte = Arte.objects.create(
            titulo='arte_teste',
            imagem='A_AULA_DE_DANÇA.png',
            preco=50,
            categoria=self.categoria        
        )
     
    def test_get_all_carrinho_itens(self):
        response = self.client.get(reverse('carrinho_lista'))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_adicionar_arte_ao_carrinho(self):
        carrinho_itens = Carrinho.objects.all()
        self.assertEqual(carrinho_itens.count(), 0)
            
        response = self.client.post(reverse('carrinho_adicionar_item', kwargs={'pk': self.arte.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        self.assertEqual(carrinho_itens.count(), 1)
    
    def test_remover_arte_do_carrinho(self):
        carrinho_item = Carrinho.objects.create(usuario=self.usuario, 
                                                arte=self.arte)
        
        carrinho_itens = Carrinho.objects.all()
        self.assertEqual(carrinho_itens.count(), 1)
        
        response = self.client.post(reverse('carrinho_item_deletar', kwargs={'pk': carrinho_item.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(carrinho_itens.count(), 0)
        
    def test_soma_dos_valores_no_carrinho(self):
        Carrinho.objects.create(usuario=self.usuario, arte=self.arte)    
        preco_total = 0
        
        for item in Carrinho.objects.all():
            preco_total += item.arte.preco
            
        self.assertEqual(preco_total, 50)