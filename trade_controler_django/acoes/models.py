from pathlib import Path
from typing import List

from django.conf import settings
from django.db import models
from django.db.models import Q


# Create your models here.

class Segmento(models.Model):
    class Meta:
        db_table = "segmentos"

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'


class SubSetor(models.Model):
    class Meta:
        db_table = "subsetores"

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'


class Setor(models.Model):
    class Meta:
        db_table = "setores"

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'


class Acao(models.Model):
    class Meta:
        db_table = "acoes"

    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=6)
    nome = models.CharField(max_length=60)
    cotacao = models.DecimalField(decimal_places=2, max_digits=10)
    variacao = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING)
    subsetor = models.ForeignKey(SubSetor, on_delete=models.DO_NOTHING)
    segmento = models.ForeignKey(Segmento, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @property
    def cover_img(self):
        return self._get_image('cover')

    @property
    def avatar_img(self):
        return self._get_image('avatar')
 
    def _get_image(self, _type:str):
        image_name = Path().joinpath(
            settings.STATIC_URL, 'img', 'acoes', _type, f'{self.id}.jpg'
        )
        return image_name


    @staticmethod
    def search(value: str) -> List:
        data = Acao.objects.all().filter(Q(codigo__icontains=value) | Q(nome__icontains=value))
        return data
