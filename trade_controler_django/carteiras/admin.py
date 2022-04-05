from django.contrib import admin

from .models import Carteira, HistoricoAnual, HistoricoSemanal, HistoricoMensal

# Register your models here.
admin.site.register(Carteira)
admin.site.register(HistoricoAnual)
admin.site.register(HistoricoMensal)
admin.site.register(HistoricoSemanal)

