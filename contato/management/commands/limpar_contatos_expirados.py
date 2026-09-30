"""
Comando de gerenciamento para limpeza e descarte seguro de mensagens de contato expiradas (LGPD).
Execução: python manage.py limpar_contatos_expirados [--dry-run] [--dias NUMERO]
"""
import logging
from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from contato.models import MensagemContato

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Remove com segurança mensagens de contato mais antigas que o período de retenção "
        "configurado em CONTATO_RETENCAO_DIAS ou informado via argumento --dias."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help="Simula a execução e informa quantas mensagens seriam excluídas, sem alterar o banco de dados."
        )
        parser.add_argument(
            '--dias',
            type=int,
            dest='dias',
            default=None,
            help="Sobrescreve explicitamente o período de retenção em dias (ex: --dias 180)."
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        dias_arg = options['dias']

        # Determina o período de retenção a utilizar
        dias_retencao = dias_arg if dias_arg is not None else getattr(settings, 'CONTATO_RETENCAO_DIAS', None)

        # Regra de Segurança Absoluta (Seções 93, 94 e 97 do Prompt 11):
        # Se nenhum prazo foi configurado, aborta com segurança e não exclui nada.
        if not dias_retencao or dias_retencao <= 0:
            self.stdout.write(
                self.style.WARNING(
                    "[ABORTADO COM SEGURANÇA] Nenhum período de retenção de contatos está configurado "
                    "(CONTATO_RETENCAO_DIAS não definido e argumento --dias ausente). "
                    "Nenhuma mensagem foi excluída do banco de dados."
                )
            )
            return

        limite = timezone.now() - timedelta(days=dias_retencao)
        limite_formatado = limite.strftime('%d/%m/%Y às %H:%M:%S')

        queryset_expirados = MensagemContato.objects.filter(criado_em__lt=limite)
        total_elegiveis = queryset_expirados.count()

        if dry_run:
            msg = (
                f"[DRY-RUN] Simulação de retenção ({dias_retencao} dias): "
                f"{total_elegiveis} mensagem(ns) anterior(es) a {limite_formatado} seriam excluída(s). "
                f"Nenhuma alteração foi realizada no banco de dados."
            )
            self.stdout.write(self.style.SUCCESS(msg))
            logger.info("Simulação de retenção de contatos (dry-run): %d mensagens identificadas.", total_elegiveis)
            return

        if total_elegiveis == 0:
            msg = f"Nenhuma mensagem de contato anterior a {limite_formatado} encontrada para exclusão."
            self.stdout.write(self.style.SUCCESS(msg))
            logger.info("Limpeza de contatos executada: 0 registros expirados.")
            return

        # Executa a exclusão definitiva
        total_removidos, _ = queryset_expirados.delete()

        # Log seguro e saída no console: ZERO dados pessoais (sem nomes, e-mails, telefones ou mensagens)
        msg_sucesso = (
            f"Limpeza de retenção concluída com sucesso: {total_removidos} mensagem(ns) "
            f"anterior(es) a {limite_formatado} ({dias_retencao} dias) foram excluída(s) em definitivo."
        )
        self.stdout.write(self.style.SUCCESS(msg_sucesso))
        logger.info(
            "Limpeza de contatos concluída: %d registros excluídos com base na retenção de %d dias.",
            total_removidos,
            dias_retencao
        )
