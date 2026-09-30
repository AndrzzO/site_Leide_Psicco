"""
Configuração do Django Admin para o app conteudos (Blog / Conteúdos Educativos).
Permite gerenciamento editorial completo de Categorias e Artigos com badges de status,
validação de rascunho/publicação e SEO básico.
"""
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import CategoriaArtigo, Artigo


@admin.register(CategoriaArtigo)
class CategoriaArtigoAdmin(admin.ModelAdmin):
    """Admin para categorias temáticas de artigos."""
    list_display = ('nome', 'slug', 'ordem', 'total_artigos_publicados', 'total_artigos_rascunho', 'ativo')
    list_editable = ('ordem', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'descricao')
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ('ordem', 'nome')
    readonly_fields = ('data_criacao', 'data_atualizacao')

    fieldsets = (
        ("IDENTIFICAÇÃO DA CATEGORIA", {
            "fields": ("nome", "slug", "descricao", "ordem", "ativo"),
            "description": "Categorias organizam as publicações educativas por eixo temático."
        }),
        ("METADADOS", {
            "fields": ("data_criacao", "data_atualizacao"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Artigos Publicados")
    def total_artigos_publicados(self, obj):
        return obj.artigos.filter(status=Artigo.STATUS_PUBLICADO).count()

    @admin.display(description="Rascunhos")
    def total_artigos_rascunho(self, obj):
        return obj.artigos.filter(status=Artigo.STATUS_RASCUNHO).count()


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    """Admin para artigos educativos do Blog."""
    list_display = (
        'titulo',
        'categoria',
        'badge_status',
        'destaque',
        'data_publicacao',
        'tempo_leitura_minutos',
        'autor',
        'data_atualizacao',
    )
    list_filter = ('status', 'destaque', 'categoria', 'data_publicacao')
    search_fields = ('titulo', 'resumo', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    readonly_fields = (
        'tempo_leitura_minutos',
        'data_criacao',
        'data_atualizacao',
        'preview_capa',
    )
    list_editable = ('destaque',)
    ordering = ('-data_publicacao', '-data_criacao')

    fieldsets = (
        ("IDENTIFICAÇÃO EDITORIAL", {
            "fields": (
                "titulo",
                "slug",
                "categoria",
                "autor",
                "servico_relacionado",
            ),
            "description": "Defina o título, URL limpa e vinculação institucional (autor e serviço relacionado)."
        }),
        ("STATUS E PUBLICAÇÃO", {
            "fields": (
                "status",
                "destaque",
                "data_publicacao",
            ),
            "description": "Apenas artigos com status 'Publicado' e data de publicação menor ou igual ao momento atual aparecem no site público. Artigos 'Rascunho' são privados do Admin."
        }),
        ("CONTEÚDO EDITORIAL", {
            "fields": (
                "resumo",
                "conteudo",
            ),
            "description": "Utilize Markdown seguro. Use ## para subtítulos de seção (H2) e ### para tópicos (H3). Não use # (H1), pois o H1 é exclusivo do título da página. Tags script e atributos maliciosos são automaticamente removidos por sanitização estrita."
        }),
        ("IMAGEM DE CAPA E ACESSIBILIDADE", {
            "fields": (
                "imagem_capa",
                "preview_capa",
                "texto_alternativo_imagem",
            ),
            "description": "Proporção recomendada: ~16:9. Formatos suportados: JPG, PNG, WEBP até 3MB. Preencha sempre o texto alternativo (alt) com clareza."
        }),
        ("SEO BÁSICO", {
            "fields": (
                "meta_titulo",
                "meta_descricao",
            ),
            "classes": ("collapse",),
            "description": "Campos opcionais. Caso não preenchidos, o sistema utiliza automaticamente o Título e o Resumo do artigo."
        }),
        ("MÉTRICAS E CONTROLE DO SISTEMA", {
            "fields": (
                "tempo_leitura_minutos",
                "data_criacao",
                "data_atualizacao",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Status")
    def badge_status(self, obj):
        agora = timezone.now()
        if obj.status == Artigo.STATUS_PUBLICADO:
            if obj.data_publicacao and obj.data_publicacao > agora:
                return format_html(
                    '<span style="background-color:#EBF8FF; color:#2B6CB0; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">Agendado</span>'
                )
            return format_html(
                '<span style="background-color:#E6F4EA; color:#137333; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">Publicado</span>'
            )
        return format_html(
            '<span style="background-color:#F1F3F4; color:#5F6368; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">Rascunho</span>'
        )

    @admin.display(description="Tempo Leitura")
    def tempo_leitura_minutos(self, obj):
        return f"{obj.tempo_leitura_estimado_minutos} min"

    @admin.display(description="Prévia da Capa")
    def preview_capa(self, obj):
        if obj.imagem_capa:
            return format_html(
                '<img src="{}" alt="{}" style="max-height:120px; max-width:240px; object-fit:cover; border-radius:4px; border:1px solid #ddd;" />',
                obj.imagem_capa.url,
                obj.texto_alternativo_imagem or obj.titulo
            )
        return "Sem imagem de capa cadastrada"
