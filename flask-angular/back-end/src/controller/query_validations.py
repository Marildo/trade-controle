"""
 @author Marildo Cesar 30/05/2023
"""

from webargs import fields, validate, ValidationError


def validate_group_by_operacoes(value):
    groups = {'ativo_id', 'carteira_id', 'data_encerramento', 'nota_compra_id', 'nota_venda_id'}
    items = {i.strip() for i in value.split(',')}
    match = groups.intersection(items)
    if len(match) != len(items):
        diff = items.difference(groups)
        raise ValidationError(f'Ivalid field {diff} in `{value}`.  Group by only allows the fields {groups}')
