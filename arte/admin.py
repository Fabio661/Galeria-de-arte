from django.contrib import admin
from .models.arte import Arte
from .models.comentario import Comentario

# Register your models here.

class ArteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'criado_em')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descricao')

admin.site.register(Arte, ArteAdmin)
admin.site.register(Comentario)