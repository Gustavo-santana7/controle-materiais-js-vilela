
from django.contrib import admin

from .models import Material, Movimentacao
from .services import registrar_movimentacao


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'unidade',
        'quantidade_estoque',
    )

    search_fields = ('nome',)
    list_filter = ('unidade',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = (
        'material',
        'tipo',
        'quantidade',
        'setor',
        'finalidade',
        'data_hora',
    )

    list_filter = ('tipo', 'setor')
    search_fields = ('material__nome', 'finalidade')

    readonly_fields = ('data_hora',)

    def save_model(self, request, obj, form, change):
        if change:
            return

        movimentacao = registrar_movimentacao(
            material_id=obj.material_id,
            tipo=obj.tipo,
            quantidade=obj.quantidade,
            setor=obj.setor,
            finalidade=obj.finalidade
        )

        obj.pk = movimentacao.pk
        obj.data_hora = movimentacao.data_hora

    def has_change_permission(self, request, obj=None):
        return obj is None

    def has_delete_permission(self, request, obj=None):
        return False
