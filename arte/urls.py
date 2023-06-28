from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArteList.as_view(), name='arte_lista'),
    path('publicar/', views.ArteCreate.as_view(), name='arte_criar'),
    path('editar/<int:pk>/', views.ArteUpdate.as_view(), name='arte_editar'),
    path('sobre/<int:pk>/', views.ArteDetail.as_view(), name='arte_detalhe'),
    path('deletar/<int:pk>/', views.ArteDelete.as_view(), name='arte_deletar'),
    path('sobre/<int:pk>/comentar', views.ArteDetail.as_view(), name='arte_comentar'),
    path('comentario/<int:id>/deletar/', views.ComentarioDelete.as_view(), name='arte_deletar_comentario'),
    path('comentario/<int:pk>/editar/', views.ComentarioUpdate.as_view(), name='arte_editar_comentario'),
      
]