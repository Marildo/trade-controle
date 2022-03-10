from django.db import models


# Create your models here.

class Segmento(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'

class SubSetor(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'


class Setor(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.id} - {self.nome}'


class Acao(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=6)
    nome = models.CharField(max_length=60)
    cotacao = models.DecimalField(decimal_places=2, max_digits=10)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING)
    subsetor = models.ForeignKey(SubSetor, on_delete=models.DO_NOTHING)
    segmento = models.ForeignKey(Segmento, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'
