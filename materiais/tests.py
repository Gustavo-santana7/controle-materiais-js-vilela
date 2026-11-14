

from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Material, Movimentacao
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


class ViewsTestCase(TestCase):

    def setUp(self):
        self.material = Material.objects.create(
            nome='Corda de nylon',
            unidade='kg',
            quantidade_estoque=Decimal('50.00')
        )

    def test_pagina_inicio(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_materiais(self):
        response = self.client.get('/materiais/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_movimentacoes(self):
        response = self.client.get('/movimentacoes/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_consulta_estoque(self):
        response = self.client.get('/consulta-estoque/')
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_material(self):
        response = self.client.post('/materiais/', {
            'nome': 'Fio de polipropileno',
            'unidade': 'kg',
            'quantidade': '25.00',
            'descricao': 'Material para produção'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Material.objects.filter(
                nome='Fio de polipropileno'
            ).exists()
        )

    def test_impedir_cadastro_sem_campos_obrigatorios(self):
        response = self.client.post('/materiais/', {
            'nome': '',
            'unidade': 'kg',
            'quantidade': '10'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Material.objects.count(), 1)

    def test_impedir_quantidade_negativa_no_cadastro(self):
        response = self.client.post('/materiais/', {
            'nome': 'Material inválido',
            'unidade': 'kg',
            'quantidade': '-5',
            'descricao': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Material.objects.count(), 1)

    def test_registrar_saida_pela_interface(self):
        response = self.client.post('/movimentacoes/', {
            'material': str(self.material.id),
            'tipo': 'S',
            'quantidade': '5',
            'setor': 'Distribuição',
            'finalidade': 'Amarrar redes'
        })

        self.assertEqual(response.status_code, 302)

        self.material.refresh_from_db()
        self.assertEqual(
            self.material.quantidade_estoque,
            Decimal('45.00')
        )
        self.assertEqual(Movimentacao.objects.count(), 1)

    def test_impedir_movimentacao_sem_setor(self):
        response = self.client.post('/movimentacoes/', {
            'material': str(self.material.id),
            'tipo': 'S',
            'quantidade': '5',
            'setor': '',
            'finalidade': 'Amarrar redes'
        })

        self.assertEqual(response.status_code, 200)
        self.material.refresh_from_db()
        self.assertEqual(
            self.material.quantidade_estoque,
            Decimal('50.00')
        )
        self.assertEqual(Movimentacao.objects.count(), 0)

    def test_impedir_tipo_de_movimentacao_invalido(self):
        response = self.client.post('/movimentacoes/', {
            'material': str(self.material.id),
            'tipo': 'X',
            'quantidade': '5',
            'setor': 'Distribuição',
            'finalidade': 'Amarrar redes'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movimentacao.objects.count(), 0)

    def test_impedir_quantidade_invalida_na_movimentacao(self):
        response = self.client.post('/movimentacoes/', {
            'material': str(self.material.id),
            'tipo': 'S',
            'quantidade': 'abc',
            'setor': 'Distribuição',
            'finalidade': 'Amarrar redes'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movimentacao.objects.count(), 0)

    def test_impedir_movimentacao_de_material_inexistente(self):
        response = self.client.post('/movimentacoes/', {
            'material': '99999',
            'tipo': 'S',
            'quantidade': '5',
            'setor': 'Distribuição',
            'finalidade': 'Amarrar redes'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movimentacao.objects.count(), 0)
