
from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Material
from .services import registrar_movimentacao


class MovimentacaoTestCase(TestCase):

    def setUp(self):
        self.material = Material.objects.create(
            nome='Corda de nylon',
            unidade='kg',
            quantidade_estoque=Decimal('50.00')
        )

    def test_registrar_entrada(self):
        registrar_movimentacao(
            material_id=self.material.id,
            tipo='E',
            quantidade=Decimal('10.00'),
            setor='Produção',
            finalidade='Reposição de estoque'
        )

        self.material.refresh_from_db()
        self.assertEqual(
            self.material.quantidade_estoque,
            Decimal('60.00')
        )

    def test_registrar_saida(self):
        registrar_movimentacao(
            material_id=self.material.id,
            tipo='S',
            quantidade=Decimal('5.00'),
            setor='Distribuição',
            finalidade='Amarrar redes'
        )

        self.material.refresh_from_db()
        self.assertEqual(
            self.material.quantidade_estoque,
            Decimal('45.00')
        )

    def test_impedir_saida_sem_estoque(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao(
                material_id=self.material.id,
                tipo='S',
                quantidade=Decimal('60.00'),
                setor='Distribuição',
                finalidade='Amarrar redes'
            )

        self.material.refresh_from_db()
        self.assertEqual(
            self.material.quantidade_estoque,
            Decimal('50.00')
        )

    def test_impedir_quantidade_zero(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao(
                material_id=self.material.id,
                tipo='E',
                quantidade=Decimal('0.00'),
                setor='Produção',
                finalidade='Teste'
            )
