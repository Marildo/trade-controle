from django.contrib import admin

from .models import Ativo, Setor, SubSetor, Segmento

# Register your models here.
admin.site.register(Ativo)
admin.site.register(Setor)
admin.site.register(SubSetor)
admin.site.register(Segmento)
