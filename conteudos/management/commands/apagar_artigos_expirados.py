"""Apaga artigos vencidos; executar a cada minuto no agendador do servidor."""
import time
from django.core.management.base import BaseCommand
from django.db import close_old_connections
from django.utils import timezone
from conteudos.models import Artigo


class Command(BaseCommand):
    help = 'Exclui definitivamente os artigos com prazo vencido.'

    def add_arguments(self, parser):
        parser.add_argument('--continuo', action='store_true', help='Verifica a cada 60 segundos até o processo ser encerrado.')

    def handle(self, *args, **options):
        while True:
            close_old_connections()
            total, _ = Artigo.objects.filter(apagar_em__lte=timezone.now()).delete()
            if total:
                self.stdout.write(f'{total} registro(s) excluído(s).')
            if not options['continuo']:
                return
            time.sleep(60)
