"""
Configuração do Django Admin para o app nucleo.
Organizado para fácil gestão institucional com proteção de integridade.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ConfiguracaoSite, Profissional, RedeSocial


@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    """Admin da Configuração Global (Padrão Singleton)."""
    list_display = ('nome_instituto', 'slogan_principal', 'whatsapp', 'email', 'ativo', 'data_atualizacao')
    readonly_fields = ('data_atualizacao', 'preview_logo')

    fieldsets = (
        ("IDENTIDADE INSTITUCIONAL", {
            "fields": (
                "nome_instituto",
                "razao_social",
                "slogan_principal",
                "frase_institucional",
                "frase_emocional",
                "cta_principal",
            )
        }),
        ("CANAIS DE CONTATO", {
            "fields": (
                "telefone",
                "whatsapp",
                "mensagem_whatsapp_padrao",
                "email",
                "instagram",
            )
        }),
        ("LOCALIZAÇÃO E ATENDIMENTO", {
            "fields": (
                "modalidade_atendimento",
                "endereco_texto",
                "cidade",
                "estado",
                "horario_atendimento",
                "mapa_url",
            )
        }),
        ("IDENTIDADE VISUAL E IMAGENS", {
            "fields": (
                "logo",
                "preview_logo",
                "logo_horizontal",
                "logo_vertical",
                "favicon",
                "imagem_compartilhamento_padrao",
            ),
            "description": "Logotipos institucionais e imagens de compartilhamento social (Open Graph)."
        }),
        ("STATUS E CONTROLE", {
            "fields": (
                "ativo",
                "data_atualizacao",
            )
        }),
    )

    def preview_logo(self, obj):
        """Exibe prévia segura do logo no painel administrativo."""
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; border-radius: 4px; background: #eee; padding: 4px;" alt="Logo" />',
                obj.logo.url
            )
        return "Nenhum logo enviado."
    preview_logo.short_description = "Prévia do Logo"

    def has_add_permission(self, request):
        """Impede a criação de múltiplos registros; permite adicionar apenas se nenhum existir."""
        if ConfiguracaoSite.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Protege a configuração global contra exclusão acidental."""
        return False


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    """Admin para gestão da Psicóloga Mari Menezes."""
    list_display = (
        'nome_exibicao',
        'titulo_profissional',
        'registro_profissional',
        'ativo',
        'destaque',
        'ordem',
        'data_atualizacao',
    )
    list_filter = ('ativo', 'destaque')
    list_editable = ('ativo', 'destaque', 'ordem')
    search_fields = ('nome', 'nome_exibicao', 'titulo_profissional', 'registro_profissional')
    ordering = ['ordem', 'nome']
    readonly_fields = ('data_criacao', 'data_atualizacao', 'preview_foto_principal')
    prepopulated_fields = {'slug': ('nome',)}

    fieldsets = (
        ("IDENTIFICAÇÃO", {
            "fields": (
                "nome",
                "nome_exibicao",
                "slug",
                "titulo_profissional",
                "atuacao_resumida",
                "registro_profissional",
            )
        }),
        ("APRESENTAÇÃO E BIOGRAFIA", {
            "fields": (
                "biografia_curta",
                "biografia_completa",
                "frase_destaque",
                "formacao_resumida",
            )
        }),
        ("FOTOGRAFIAS EDITORIAIS", {
            "fields": (
                "foto_principal",
                "preview_foto_principal",
                "foto_sobre",
                "foto_secundaria",
            ),
            "description": "Proporção recomendada para retratos: vertical ~4:5."
        }),
        ("PUBLICAÇÃO E EXIBIÇÃO", {
            "fields": (
                "ordem",
                "ativo",
                "destaque",
                "data_criacao",
                "data_atualizacao",
            )
        }),
    )

    def preview_foto_principal(self, obj):
        """Pré-visualização da fotografia principal da profissional."""
        if obj and obj.foto_principal:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 6px;" alt="{}" />',
                obj.foto_principal.url,
                obj.nome
            )
        return "Nenhuma foto cadastrada (utilizará placeholder)."
    preview_foto_principal.short_description = "Prévia da Foto Principal"


@admin.register(RedeSocial)
class RedeSocialAdmin(admin.ModelAdmin):
    """Admin de redes sociais."""
    list_display = ('nome', 'url', 'icone', 'ativo', 'ordem')
    list_editable = ('ativo', 'ordem')
    search_fields = ('nome', 'url')
    ordering = ['ordem', 'nome']
