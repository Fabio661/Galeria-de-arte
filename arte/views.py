from typing import Any, Dict
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, View, ListView
from django.views.generic.edit import FormMixin  
from .models.arte import Arte
from .models.comentario import Comentario
from .models.categoria import Categoria
from .forms import ComentarioForm
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse

# Create your views here.

class Home(TemplateView):
    template_name = 'arte_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['artes'] = Arte.objects.all()
        context['preco'] = Arte.preco
        context['descricao'] = Arte.descricao
        return context

class ArteCreate(CreateView):
    model = Arte
    fields = ('titulo', 'imagem', 'descricao', 'preco', 'categoria',)
    success_url = reverse_lazy('arte_lista')
    
class ArteUpdate(UpdateView):
    model = Arte
    fields = ('titulo', 'imagem', 'descricao', 'preco', 'categoria',)
    success_url = reverse_lazy('arte_lista')

class ArteDetail(FormMixin, DetailView):
    queryset = Arte.objects.all()
    form_class = ComentarioForm
    
    def get_success_url(self):
        return reverse('arte_detalhe', kwargs={'pk':self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super(ArteDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    #Comentar    
    def post(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            form = ComentarioForm(request.POST)
            if form.is_valid():
                novo_comentario = form.save(commit=False)
                novo_comentario.arte = Arte.objects.get(id=pk)
                novo_comentario.save()
                return HttpResponseRedirect(request.path_info)
            else:
                novo_comentario = ComentarioForm()
    
class ArteDelete(DeleteView):
    queryset = Arte.objects.all()
    success_url = reverse_lazy('arte_lista')
    
class ComentarioDelete(View):
    
    def get_success_url(self):
        return reverse('arte_detalhe', kwargs={'pk':self.object.pk})
    
    def get(self, request, id):
        comentario = get_object_or_404(Comentario, id=id)
        return render(request, 'arte/comentario_delete.html', context={'comentario':comentario})
    
    def post(self, request, id):
        comentario = get_object_or_404(Comentario, id=id)
        comentario.delete()
        return redirect(reverse('arte_lista'))

class ComentarioUpdate(UpdateView):
    model = Comentario
    fields = ('comentario',)
    success_url = reverse_lazy('arte_lista')
    
class ArtesFiltradas(TemplateView):
    template_name = 'arte_list_filtrada.html'
    
    def get_success_url(self):
        return reverse('artes_filtradas', kwargs={'slug':self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        artes_filtradas = Arte.objects.filter(categoria=categoria)
        context['artes_filtradas'] = artes_filtradas
        context['preco'] = Arte.preco
        context['categoria'] = categoria
        return context
    
class EncontrarArtes(ListView):
    model = Arte
    artes = Arte.objects.all()
    template_name = 'encontrar_arte.html'
    
    def get_queryset(self):
        encontrar_titulo = self.request.GET.get('titulo')
           
        if encontrar_titulo:    
            artes = Arte.objects.filter(titulo__icontains=encontrar_titulo)
        else:
            artes = Arte.objects.all()
            
        return artes