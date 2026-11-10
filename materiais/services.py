
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Material, Movimentacao


@transaction.atomic
def registrar_movimentacao(
    material_id,
    tipo,
    quantidade,
    setor,
    finalidade
):
    material = Material.objects.select_for_update().get(
        id=material_id
    )

    if quantidade <= 0:
        raise ValidationError(
            'A quantidade deve ser maior que zero.'
        )

    if tipo == 'S' and quantidade > material.quantidade_estoque:
        raise ValidationError(
            'Estoque insuficiente para realizar esta saída.'
        )

    if tipo == 'E':
        material.quantidade_estoque += quantidade

    elif tipo == 'S':
        material.quantidade_estoque -= quantidade

    else:
        raise ValidationError(
            'Tipo de movimentação inválido.'
        )

    material.save(update_fields=['quantidade_estoque'])

    movimentacao = Movimentacao.objects.create(
        material=material,
        tipo=tipo,
        quantidade=quantidade,
        setor=setor,
        finalidade=finalidade
    )

    return movimentacao
