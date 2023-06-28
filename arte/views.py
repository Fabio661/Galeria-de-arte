from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.views.generic.edit import FormMixin, DeletionMixin
from .models.arte import Arte
from .models.comentario import Comentario
from .forms import ComentarioForm
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse

# Create your views here.

class ArteList(ListView):
    model = Arte
    queryset = Arte.objects.all()

class ArteCreate(CreateView):
    model = Arte
    fields = ('titulo', 'imagem', 'descricao', 'preco', 'categoria',)
    success_url = reverse_lazy('arte_lista')
    
class ArteUpdate(UpdateView):
    model = Arte
    fields = ('titulo', 'imagem', 'descricao', 'preco', 'categoria',)
    success_url = reverse_lazy('arte_lista')

class ArteDetail(DeletionMixin, FormMixin, DetailView):
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