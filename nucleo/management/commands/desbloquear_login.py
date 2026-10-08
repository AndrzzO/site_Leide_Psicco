from django.core.management.base import BaseCommand
from nucleo.models import BloqueioLogin
from nucleo.rate_limit import gerar_digest_origem
import ipaddress


class Command(BaseCommand):
    help = 'Remove bloqueio e histórico de falhas de um IP autorizado.'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=ipaddress.ip_address)

    def handle(self, *args, **options):
        total, _ = BloqueioLogin.objects.filter(origem=gerar_digest_origem('login', str(options['ip']))).delete()
        self.stdout.write(f'{total} bloqueio(s) removido(s).')
