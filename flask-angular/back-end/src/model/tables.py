"""
 @author Marildo Cesar 24/04/2023
"""
from abc import ABC

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, CHAR, FLOAT, DATE, DATETIME, TIMESTAMP, BOOLEAN, Enum, text, ForeignKey
from sqlalchemy.orm import relationship

from .enums import TipoAtivo, TipoNota, TipoCarteira
from .fields import primary_key

Base = declarative_base()


class Setor(Base):
    __tablename__ = 'setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))

    subsetores = relationship("SubSetor", uselist=True, back_populates="setores")
    segmentos = relationship("Segmento", uselist=True, back_populates="setores")

    def __str__(self) -> str:
        return f'{self.id} - {self.nome}'


class SubSetor(Base):
    __tablename__ = 'sub_setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))


class Segmento(Base):
    __tablename__ = 'segmentos'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))


class Ativo(Base):
    __tablename__ = 'ativos'
    id = Column(INTEGER, primary_key=True)
    master_id = Column(INTEGER, default=0)
    tipo = Column(Enum(TipoAtivo))
    codigo = Column(CHAR(6))
    nome = Column(VARCHAR(60))
    cotacao = Column(FLOAT(precision=3))
    variacao = Column(FLOAT(precision=3))
    update_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))
    setor = relationship("Setor", back_populates="ativos")

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Carteira(Base):
    __tablename__ = 'carteiras'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(40))
    saldo_ativos = Column(FLOAT, default=0)
    saldo_caixa = Column(FLOAT, default=0)
    tipo = Column(Enum(TipoCarteira))
    daytrade = Column(BOOLEAN, default=False, nullable=False)


class NotaCorretagem(Base):
    __tablename__ = 'notas_corretagem'
    id = Column(INTEGER, primary_key=True)
    comprovante = Column(INTEGER, nullable=False)
    data_referencia = Column(DATE, nullable=False)
    data_upload = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    tipo = Column(Enum(TipoNota))


class Operacoes(Base):
    __tablename__ = 'operacoes'

    id = primary_key
    data_compra = Column(DATETIME, nullable=True)
    data_venda = Column(DATETIME, nullable=True)
    pm_compra = Column(FLOAT, default=0)
    pm_venda = Column(FLOAT, default=0)
    quantidade = Column(FLOAT, default=0)
    custos = Column(FLOAT, default=0)
    irpf = Column(FLOAT, default=0)
    outros = Column(FLOAT, default=0)
    daytrade = Column(BOOLEAN, default=False, nullable=False)
    encerrada = Column(BOOLEAN, default=False, nullable=False)
    data_encerramento = Column(DATE, nullable=True)
    ativo_id = Column(INTEGER, ForeignKey('ativos.id'))
    ativo = relationship("Ativo", back_populates='operacoes')
    carteira_id = Column(INTEGER, ForeignKey('carteiras.id'))
    carteira = relationship("Carteira", back_populates='operacoes')
    nota_id = Column(INTEGER, ForeignKey('notas_corretagem.id'))
    nota = relationship("Nota", back_populates='operacoes')