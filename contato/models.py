"""
Modelos do app contato:
- MensagemContato: Registro mínimo e seguro de mensagens enviadas por visitantes
  do site para iniciar contato institucional ou tirar dúvidas sobre atendimentos.
"""
from django.db import models


class MensagemContato(models.Model):
    """
    Model de contato institucional regido pelo princípio da minimização de dados (LGPD).
    Coleta exclusivamente os dados necessários para que a equipe do Instituto retorne
    a mensagem do visitante. Não constitui prontuário, ficha clínica ou CRM.
    """
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome Completo",
        help_text="Nome informado pelo visitante para identificação no contato."
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
        help_text="E-mail para resposta. Obrigatório se o telefone não for informado."
    )
    telefone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Telefone / WhatsApp",
        help_text="Telefone com DDD para contato. Obrigatório se o e-mail não for informado."
    )
    servico_interesse = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'ativo': True},
        related_name='mensagens_contato',
        verbose_name="Serviço ou Assunto de Interesse",
        help_text="Serviço do Instituto sobre o qual o visitante busca informações (opcional)."
    )
    mensagem = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Mensagem Breve",
        help_text="Texto informativo breve sobre o contato (limite de até 2000 caracteres)."
    )
    aceite_privacidade = models.BooleanField(
        default=False,
        verbose_name="Aceite da Política de Privacidade",
        help_text="Confirmação de que o visitante leu e concorda com a Política de Privacidade."
    )
    lida = models.BooleanField(
        default=False,
        verbose_name="Mensagem Lida",
        help_text="Controle administrativo interno para identificar mensagens já respondidas ou analisadas."
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Envio"
    )

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-criado_em']

    def __str__(self):
        data_formatada = self.criado_em.strftime('%d/%m/%Y às %H:%M') if self.criado_em else 'Data pendente'
        return f"Contato de {self.nome} — {data_formatada}"
