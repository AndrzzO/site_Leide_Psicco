"""
Configuração do Django Admin para o app contato.
Permite gestão segura das mensagens recebidas pelo site, com triagem de leitura,
campos de conteúdo em modo somente leitura (readonly) para integridade e preservação de privacidade.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import MensagemContato


@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    """
    Administração de mensagens de contato.
    Os dados enviados pelo visitante são estritamente mantidos como readonly para preservar
    sua integridade original. Apenas o status de leitura pode ser modificado pelos operadores.
    """
    list_display = (
        'nome',
        'servico_interesse',
        'email',
        'telefone',
        'badge_status_leitura',
        'lida',
        'criado_em',
    )
    list_editable = ('lida',)
    list_filter = ('lida', 'servico_interesse', 'criado_em')
    search_fields = ('nome', 'email', 'telefone')
    date_hierarchy = 'criado_em'
    ordering = ('-criado_em',)

    readonly_fields = (
        'nome',
        'email',
        'telefone',
        'servico_interesse',
        'mensagem_segura',
        'aceite_privacidade',
        'criado_em',
    )

    fieldsets = (
        ("DADOS DO VISITANTE", {
            "fields": ("nome", "email", "telefone", "servico_interesse"),
            "description": "Dados informados pelo visitante para que a clínica possa retornar o contato."
        }),
        ("CONTEÚDO DA MENSAGEM", {
            "fields": ("mensagem_segura",),
            "description": "Mensagem breve enviada pelo site. Lembrete: este canal não deve ser utilizado como prontuário, ficha clínica ou para armazenamento de dados médicos."
        }),
        ("CONSENTIMENTO E AUDITORIA", {
            "fields": ("aceite_privacidade", "criado_em", "lida"),
            "description": "Registro de conformidade e controle administrativo de atendimento."
        }),
    )

    @admin.display(description="Status")
    def badge_status_leitura(self, obj):
        if obj.lida:
            return format_html(
                '<span style="background-color:#E6F4EA; color:#137333; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">{}</span>',
                'Respondida / Lida'
            )
        return format_html(
            '<span style="background-color:#FCE8E6; color:#C5221F; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">{}</span>',
            'Nova Mensagem'
        )

    @admin.display(description="Mensagem do Visitante")
    def mensagem_segura(self, obj):
        if not obj.mensagem:
            return format_html('<em>Nenhuma mensagem de texto inserida.</em>')
        return format_html(
            '<div style="background:#FBF9F5; padding:12px 16px; border-radius:6px; border:1px solid #E2DED4; max-width:700px; white-space:pre-wrap; font-family:sans-serif; font-size:13px; line-height:1.6; color:#2C3C30;">{}</div>',
            obj.mensagem
        )

    actions = ['marcar_como_lida', 'marcar_como_nao_lida']

    @admin.action(description="Marcar mensagens selecionadas como lidas")
    def marcar_como_lida(self, request, queryset):
        queryset.update(lida=True)

    @admin.action(description="Marcar mensagens selecionadas como não lidas")
    def marcar_como_nao_lida(self, request, queryset):
        queryset.update(lida=False)

    def has_add_permission(self, request):
        # Mensagens de contato só podem ser originadas através do formulário web do site
        return False

