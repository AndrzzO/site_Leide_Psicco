from django.test import Client
from html.parser import HTMLParser
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and ('site-header__cta' in a.get('class','') or 'site-header__mobile-cta' in a.get('class','')):
            assert a['href']=='/contato/?assunto=consulta#formulario-contato'
            assert 'target' not in a
            print('Agendamento interno confirmado:',a['href'])
r=Client().get('/')
assert r.status_code==200
Links().feed(r.content.decode())
