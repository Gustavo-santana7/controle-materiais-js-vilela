
from django.db import models
from django.core.validators import MinValueValidator


class Material(models.Model):
    UNIDADES = [
        ('kg', 'Quilograma'),
        ('m', 'Metro'),
        ('un', 'Unidade'),
    ]

    nome = models.CharField(max_length=100)
    unidade = models.CharField(
        max_length=2,
        choices=UNIDADES
    )
    quantidade_estoque = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome



class Movimentacao(models.Model):
    TIPOS = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='movimentacoes'
    )

    tipo = models.CharField(
        max_length=1,
        choices=TIPOS
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    setor = models.CharField(max_length=100)

    finalidade = models.CharField(max_length=200)

    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_hora']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.material.nome}'
