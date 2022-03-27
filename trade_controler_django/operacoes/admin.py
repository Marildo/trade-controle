from django.contrib import admin

from .models import Operacao


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('ativo', 'quantidade', 'data_compra')


admin.site.register(Operacao, OperacaoAdmin)

