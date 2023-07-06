from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/<int:pk>/carrinho/', views.AdicionarArteCarrinho.as_view(), name='carrinho_adicionar_item'),
    path('carrinho/', views.CarrinhoItens.as_view(), name='carrinho_lista'),
    path('carrinho/<int:pk>/', views.DeletarArteCarrinho.as_view(), name='carrinho_item_deletar')
]
