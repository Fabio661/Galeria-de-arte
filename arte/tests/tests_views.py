from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from arte.factories import UsuarioFactory, CategoriaFactory
from arte.models.arte import Arte




class ArteTeste(TestCase):
    
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
        
    def test_get_all_artes(self):
        response = self.client.get(reverse('arte_lista'))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_arte(self):
        response = self.client.get(reverse('arte_detalhe', args=([self.arte.id])))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_criar_arte(self):     
        data = {
            'titulo': 'titulo_teste',
            'preco': 20
        }
        
        response = self.client.post(reverse('arte_criar'), data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND) 
        
        arte_criada = Arte.objects.get(titulo='titulo_teste')
        self.assertEqual(arte_criada.titulo, 'titulo_teste')

    def test_deletar_arte(self):
        arte = Arte.objects.get(titulo='arte_teste')
        self.assertEqual(arte.titulo, 'arte_teste')
        
        artes = Arte.objects.all()
        
        response = self.client.post(reverse('arte_deletar',kwargs={'pk': arte.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(artes.count(), 0)

    def test_editar_arte(self):
        arte = Arte.objects.get(titulo='arte_teste')
        categoria = CategoriaFactory(titulo='categotia_teste',
                                     slug='categoria-teste',
                                     descricao='categoria descricao teste')
        
        response = self.client.post(reverse('arte_editar', kwargs={'pk': arte.id}),
                                    {'titulo': 'arte_teste_atualizado',
                                     'imagem': 'A_AULA_DE_DANÇA.png',
                                     'descricao': 'teste_descricao',
                                     'preco': 30,
                                     'categoria': categoria.id
                                    })
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)     
        arte.refresh_from_db()
        self.assertEqual(arte.titulo, 'arte_teste_atualizado')
        
    def test_filtrar_arte_por_categoria(self):
        response = self.client.get(reverse('artes_filtradas', kwargs={'slug': self.arte.categoria}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.arte.categoria, self.categoria)
        
    def test_encontrar_arte_pelo_titulo(self):        
        arte_encontrada = Arte.objects.filter(titulo='arte_teste')             
        qs = Arte.objects.filter(titulo__icontains=self.arte.titulo)
        
        self.assertQuerysetEqual(qs, arte_encontrada)