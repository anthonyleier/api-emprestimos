from django.contrib import admin
from onidata.models import Emprestimo, Pagamento


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor_nominal', 'taxa_juros', 'ip', 'data', 'banco', 'cliente', 'usuario']
    list_display_links = ['id']
    list_filter = ['usuario', 'data']
    search_fields = ['banco', 'cliente']
    list_per_page = 20
    ordering = ['-id']


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'emprestimo', 'valor', 'data', 'usuario']
    list_display_links = ['id']
    list_filter = ['usuario', 'data']
    list_per_page = 20
    ordering = ['-id']
