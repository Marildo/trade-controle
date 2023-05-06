"""
 @author Marildo Cesar 24/04/2023
"""

from typing import List

from sqlalchemy import (Column, Index, INTEGER, VARCHAR, CHAR, FLOAT, DATE, DATETIME, TIMESTAMP, BOOLEAN, Enum,
                        text, ForeignKey)
from sqlalchemy.orm import relationship
from .init_db import db_connection, Base
from .enums import TipoInvestimento, TipoNota, TipoCarteira, CompraVenda, NotaStatusProcess
from .fields import primary_key


class BaseTable(Base):
    __abstract__ = True

    def save(self):
        with db_connection as conn:
            conn.session.merge(self)
            conn.session.flush()
            conn.session.commit()


class Setor(BaseTable):
    __tablename__ = 'setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    subsetores = relationship("SubSetor", uselist=True, backref='setores')

    def __str__(self) -> str:
        return f'{self.id} - {self.nome}'


class SubSetor(BaseTable):
    __tablename__ = 'sub_setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))


class Segmento(BaseTable):
    __tablename__ = 'segmentos'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))


class Ativo(BaseTable):
    __tablename__ = 'ativos'
    id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER, default=0)
    codigo = Column(CHAR(6))
    nome = Column(VARCHAR(60))
    descricao = Column(VARCHAR(90))
    cotacao = Column(FLOAT(precision=3))
    variacao = Column(FLOAT(precision=3))
    tipo_ativo = Column(VARCHAR(6), nullable=True)
    tipo_investimento = Column(Enum(TipoInvestimento))
    update_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))
    setor = relationship("Setor")
    segmento_id = Column(INTEGER, ForeignKey('segmentos.id'))
    segmento = relationship("Segmento")

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @staticmethod
    def find_like_name(nome: str):
        with db_connection as conn:
            query = conn.session.query(Ativo).filter(Ativo.nome.ilike(f'%{nome.strip()}%'))
            return query.all()


class Carteira(BaseTable):
    __tablename__ = 'carteiras'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(40))
    saldo_ativos = Column(FLOAT, default=0)
    saldo_caixa = Column(FLOAT, default=0)
    tipo = Column(Enum(TipoCarteira))
    daytrade = Column(BOOLEAN, default=False, nullable=False)


class NotaCorretagem(BaseTable):
    __tablename__ = 'notas_corretagem'
    id = Column(INTEGER, primary_key=True)
    comprovante = Column(INTEGER)
    data_referencia = Column(DATE)
    data_upload = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    data_processamento = Column(DATETIME)
    pdf_name = Column(VARCHAR(120))
    tipo = Column(Enum(TipoNota))
    status = Column(Enum(NotaStatusProcess))
    __table_args__ = (Index('idx_comprovante_tipo', 'comprovante', 'tipo', 'pdf_name', unique=True),)

    def __str__(self):
        return f'Data: {self.data_referencia} - Comprovante: {self.comprovante} - Tipo: {self.tipo}'

    def is_exists(self) -> bool:
        with db_connection as conn:
            query = (conn.session.query(NotaCorretagem)
                     .filter(NotaCorretagem.pdf_name == self.pdf_name,
                             NotaCorretagem.tipo == self.tipo,
                             NotaCorretagem.status != NotaStatusProcess.ERROR)
                     )
            return query.count() > 0

    @staticmethod
    def read_by_params(params) -> List:
        with db_connection as conn:
            query = (conn.session.query(NotaCorretagem)
                     )
            return query.all()


class Operacao(BaseTable):
    __tablename__ = 'operacoes'

    id = primary_key
    data_compra = Column(DATE, nullable=True)
    data_venda = Column(DATE, nullable=True)
    pm_compra = Column(FLOAT(precision=2), default=0)
    pm_venda = Column(FLOAT(precision=2), default=0)
    qtd_compra = Column(FLOAT(precision=2), default=0)
    qtd_venda = Column(FLOAT(precision=2), default=0)
    custos = Column(FLOAT(precision=4), default=0)
    irpf = Column(FLOAT(precision=4), default=0)
    daytrade = Column(BOOLEAN, default=False, nullable=False)
    encerrada = Column(BOOLEAN, default=False, nullable=False)
    data_encerramento = Column(DATE, nullable=True)
    compra_venda = Column(Enum(CompraVenda))
    ativo_id = Column(INTEGER, ForeignKey('ativos.id'))
    ativo = relationship("Ativo")
    carteira_id = Column(INTEGER, ForeignKey('carteiras.id'))
    carteira = relationship("Carteira")
    nota_compra_id = Column(INTEGER, ForeignKey('notas_corretagem.id'))
    nota_compra = relationship("NotaCorretagem", foreign_keys=[nota_compra_id], lazy=True)
    nota_venda_id = Column(INTEGER, ForeignKey('notas_corretagem.id'))
    nota_venda = relationship("NotaCorretagem", foreign_keys=[nota_venda_id], lazy=True)

    def __init__(self):
        self.qtd_compra = 0.0
        self.qtd_venda = 0.0
        self.pm_venda = 0.0
        self.pm_compra = 0.0
        self.custos = 0.0
        self.irpf = 0.0

    @property
    def qtd_aberta(self):
        return self.qtd_compra - self.qtd_venda

    @staticmethod
    def find_not_closed(ativo: Ativo, compra_venda: CompraVenda, daytrade: bool) -> List:
        with db_connection as conn:
            filters = [Operacao.compra_venda == compra_venda,
                       Operacao.encerrada == False,
                       Operacao.daytrade == daytrade]
            query = (conn.session.query(Operacao)
                     .join(Ativo, Operacao.ativo_id == ativo.id)
                     .filter(*filters)).all()

            return query
