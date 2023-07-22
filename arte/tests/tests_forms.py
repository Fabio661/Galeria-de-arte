from django.test import TestCase
from rest_framework import status
from factories import UsuarioFactory, ArteFactory
from arte.models.comentario import Comentario
from arte.forms import ComentarioForm
from django.urls import reverse

class ComentarioTeste(TestCase):
    
    def setUp(self):
        
        self.usuario = UsuarioFactory(username='usuario_teste')
        
        self.client.force_login(user=self.usuario)
        
        self.arte = ArteFactory(
            titulo='titulo',
            preco=20
        )
        
    def test_fazer_comentario(self):
        data = {
            'usuario': self.usuario,
            'arte': self.arte,
            'comentario': 'muito bom',
        }
        
        form = ComentarioForm(data=data)
        
        if form.is_valid():
           comentario = Comentario.objects.create(usuario=self.usuario, arte=self.arte)
        
        comentario_criado = Comentario.objects.get(arte=self.arte)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(comentario, comentario_criado)
    
    def test_deletar_comentario(self):
        comentario = Comentario.objects.create(usuario=self.usuario, arte=self.arte, comentario='ok')      
        
        self.assertEqual(comentario.comentario, 'ok')
        
        comentarios = Comentario.objects.all()
        
        response = self.client.post(reverse('arte_deletar_comentario', kwargs={'id': comentario.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(comentarios.count(), 0)
        
    def test_editar_comentario(self):
        comentario = Comentario.objects.create(usuario=self.usuario, arte=self.arte, comentario='Gostei')
        self.assertEqual(comentario.comentario, 'Gostei')
        
        data = {
            'comentario': 'Não Gostei'
        }
        
        response = self.client.post(reverse('arte_editar_comentario', kwargs={'pk': comentario.id}), data=data)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        comentario.refresh_from_db()
        self.assertEqual(comentario.comentario, 'Não Gostei')