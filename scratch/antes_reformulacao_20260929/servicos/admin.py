"""
Configuração do Django Admin para o app servicos.
Gestão de Áreas de Atuação e Catálogo de Serviços Clínicos / Avaliativos.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import AreaAtuacao, Servico


@admin.register(AreaAtuacao)
class AreaAtuacaoAdmin(admin.ModelAdmin):
    """Admin para as grandes Áreas de Atuação (Home e estrutura institucional)."""
    list_display = ('nome', 'titulo', 'ativo', 'mostrar_na_home', 'ordem', 'data_atualizacao')
    list_filter = ('ativo', 'mostrar_na_home')
    list_editable = ('ativo', 'mostrar_na_home', 'ordem')
    search_fields = ('nome', 'titulo', 'resumo')
    ordering = ['ordem', 'nome']
    readonly_fields = ('data_criacao', 'data_atualizacao', 'preview_imagem')
    prepopulated_fields = {'slug': ('nome',)}

    fieldsets = (
        ("IDENTIFICAÇÃO DA ÁREA", {
            "fields": (
                "nome",
                "slug",
                "titulo",
                "ordem",
                "ativo",
                "mostrar_na_home",
            )
        }),
        ("CONTEÚDO DO CARD E DETALHAMENTO", {
            "fields": (
                "resumo",
                "descricao",
                "frase_destaque",
            )
        }),
        ("FOTOGRAFIA DO CARD", {
            "fields": (
                "imagem",
                "preview_imagem",
                "texto_alternativo_imagem",
            ),
            "description": "Proporção recomendada: ~4:3."
        }),
        ("METADADOS", {
            "fields": (
                "data_criacao",
                "data_atualizacao",
            )
        }),
    )

    def preview_imagem(self, obj):
        """Pré-visualização segura da imagem da área."""
        if obj and obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 4px;" alt="{}" />',
                obj.imagem.url,
                obj.nome
            )
        return "Nenhuma imagem cadastrada (utilizará placeholder)."
    preview_imagem.short_description = "Prévia da Imagem"


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    """Admin para os Serviços, Psicoterapias e Avaliações."""
    list_display = ('nome', 'area', 'ativo', 'mostrar_na_home', 'ordem', 'data_atualizacao')
    list_filter = ('ativo', 'mostrar_na_home', 'area')
    list_editable = ('ativo', 'mostrar_na_home', 'ordem')
    search_fields = ('nome', 'titulo', 'subtitulo', 'resumo')
    ordering = ['ordem', 'nome']
    readonly_fields = ('data_criacao', 'data_atualizacao', 'preview_imagem')
    prepopulated_fields = {'slug': ('nome',)}

    fieldsets = (
        ("IDENTIFICAÇÃO E ENQUADRAMENTO", {
            "fields": (
                "nome",
                "slug",
                "area",
                "icone",
                "ordem",
                "ativo",
                "mostrar_na_home",
            )
        }),
        ("CONTEÚDO EDITORIAL", {
            "fields": (
                "titulo",
                "subtitulo",
                "resumo",
                "descricao",
                "frase_destaque",
            )
        }),
        ("IMAGEM DA PÁGINA", {
            "fields": (
                "imagem_principal",
                "preview_imagem",
                "texto_alternativo_imagem",
            ),
            "description": "Proporção recomendada: horizontal ~16:9."
        }),
        ("OTIMIZAÇÃO PARA BUSCADORES (SEO)", {
            "fields": (
                "meta_titulo",
                "meta_descricao",
            ),
            "description": "Campos opcionais para personalização de títulos e resumos para o Google."
        }),
        ("METADADOS", {
            "fields": (
                "data_criacao",
                "data_atualizacao",
            )
        }),
    )

    def preview_imagem(self, obj):
        """Pré-visualização segura da imagem principal do serviço."""
        if obj and obj.imagem_principal:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 4px;" alt="{}" />',
                obj.imagem_principal.url,
                obj.nome
            )
        return "Nenhuma imagem cadastrada (utilizará placeholder)."
    preview_imagem.short_description = "Prévia da Imagem"
