from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from .services import registrar_movimentacao

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Material, Movimentacao


def inicio(request):
    total_materiais = Material.objects.count()

    movimentacoes_recentes = (
        Movimentacao.objects
        .select_related('material')
        .all()[:5]
    )

    contexto = {
        'total_materiais': total_materiais,
        'movimentacoes_recentes': movimentacoes_recentes,
    }

    return render(request, 'materiais/inicio.html', contexto)


def materiais(request):
    lista_materiais = Material.objects.all().order_by('nome')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        unidade = request.POST.get('unidade', '').strip()
        quantidade = request.POST.get('quantidade', '').strip()
        descricao = request.POST.get('descricao', '').strip()

        if not nome or not unidade or not quantidade:
            messages.error(request, 'Preencha os campos obrigatórios.')
        else:
            try:
                from decimal import Decimal, InvalidOperation

                valor = Decimal(quantidade)

                if valor < 0:
                    raise InvalidOperation

                Material.objects.create(
                    nome=nome,
                    unidade=unidade,
                    quantidade_estoque=valor,
                    descricao=descricao
                )

                messages.success(request, 'Material cadastrado com sucesso.')
                return redirect('materiais')

            except (InvalidOperation, ValueError):
                messages.error(request, 'Informe uma quantidade válida.')

    contexto = {
        'lista_materiais': lista_materiais,
        'unidades': Material.UNIDADES,
    }

    return render(request, 'materiais/materiais.html', contexto)


def movimentacoes(request):
    lista_materiais = Material.objects.all().order_by('nome')

    if request.method == 'POST':
        try:
            material_id = int(request.POST.get('material'))
            tipo = request.POST.get('tipo', '').strip()
            quantidade = Decimal(request.POST.get('quantidade', ''))
            setor = request.POST.get('setor', '').strip()
            finalidade = request.POST.get('finalidade', '').strip()

            if not setor or not finalidade:
                raise ValidationError(
                    'Preencha o setor e a finalidade.'
                )

            if tipo not in ('E', 'S'):
                raise ValidationError(
                    'Selecione um tipo de movimentação válido.'
                )

            registrar_movimentacao(
                material_id=material_id,
                tipo=tipo,
                quantidade=quantidade,
                setor=setor,
                finalidade=finalidade
            )

            messages.success(
                request,
                'Movimentação registrada com sucesso!'
            )
            return redirect('movimentacoes')

        except (InvalidOperation, ValueError, TypeError):
            messages.error(
                request,
                'Verifique os dados informados.'
            )

        except ValidationError as erro:
            messages.error(request, ' '.join(erro.messages))

        except Material.DoesNotExist:
            messages.error(request, 'Material não encontrado.')

    contexto = {
        'lista_materiais': lista_materiais,
        'tipos': Movimentacao.TIPOS,
        'historico': Movimentacao.objects.select_related(
            'material'
        ).all()[:10],
    }

    return render(
        request,
        'materiais/movimentacoes.html',
        contexto
    )


def consulta_estoque(request):
    lista_materiais = Material.objects.all().order_by('nome')

    contexto = {
        'lista_materiais': lista_materiais,
        'total_materiais': lista_materiais.count(), 
    }

    return render(
        request,
        'materiais/consulta_estoque.html',
        contexto
    )