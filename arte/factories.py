import factory

from django.contrib.auth.models import User
from arte.models.arte import Arte
from arte.models.categoria import Categoria
from arte.models.comentario import Comentario

class UsuarioFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('pystr')
    
    class Meta:
        model = User
              
class CategoriaFactory(factory.django.DjangoModelFactory):
    titulo = factory.Faker('pystr')
    slug = factory.Faker("pystr")
    descricao = factory.Faker("pystr")
    
    class Meta:
        model = Categoria
        
class ArteFactory(factory.django.DjangoModelFactory):
    titulo = factory.Faker('pystr')
    preco = factory.Faker('pyint')
    
    class Meta:
        model = Arte