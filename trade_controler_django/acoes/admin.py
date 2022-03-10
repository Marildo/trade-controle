from django.contrib import admin

from .models import Acao, Setor, SubSetor, Segmento

# Register your models here.
admin.site.register(Acao)
admin.site.register(Setor)
admin.site.register(SubSetor)
admin.site.register(Segmento)
