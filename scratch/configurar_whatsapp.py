from nucleo.models import ConfiguracaoSite
config = ConfiguracaoSite.objects.filter(ativo=True).first()
if config is None:
    config = ConfiguracaoSite(ativo=True)
config.whatsapp = '5561993147966'
config.mensagem_whatsapp_padrao = 'Olá, psicóloga Mari Menezes!\n\nConheci o Instituto Mente em Foco pelo site e gostaria de informações sobre atendimento psicológico ou avaliação neuropsicológica.\n\nVocê poderia me informar como funciona o atendimento e quais horários estão disponíveis?\n\nObrigada(o)!'
config.save()
from urllib.parse import urlparse, parse_qs
link = urlparse(config.whatsapp_link)
assert link.netloc == 'wa.me' and link.path == '/5561993147966'
assert parse_qs(link.query)['text'][0] == config.mensagem_whatsapp_padrao
print('WhatsApp e mensagem configurados e verificados.')
