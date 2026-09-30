from pathlib import Path
import re
def read(p): return Path(p).read_text(encoding='utf-8-sig')
def write(p,s): Path(p).write_text(s,encoding='utf-8')
p='templates/componentes/menu_mobile.html';s=read(p);s=re.sub(r'{#(.*?)#}',r'{% comment %}\1{% endcomment %}',s,flags=re.S);write(p,s)
p='templates/paginas/home.html';s=read(p).replace('height="1024" fetchpriority', 'height="1024" loading="eager" fetchpriority');write(p,s)
for p,typ in [('templates/servicos/psicologia.html','Psicoterapia Clínica'),('templates/servicos/avaliacao_hub.html','Avaliação Psicológica'),('templates/servicos/avaliacao_especifica.html','Avaliação Psicológica')]:
    s=read(p).replace('{% render_breadcrumbs_schema breadcrumb %}', '{% render_breadcrumbs_schema breadcrumb %}{% render_service_schema servico "'+typ+'" %}')
    write(p,s)
p='paginas/views.py';s=read(p).replace('Avaliações Psicológicas, Laudos e Pareceres | Mari Menezes','Avaliações, Laudos e Pareceres | Instituto Mente em Foco');write(p,s)
p='servicos/views.py';s=read(p).replace('Avaliações Psicológicas, Laudos e Pareceres | Mente em Foco','Avaliações, Laudos e Pareceres | Instituto Mente em Foco').replace("item['h1'] + ' | Mente em Foco'", "item['h1'] + ' | Instituto Mente em Foco'");write(p,s)
p='nucleo/templatetags/seo_tags.py';s=read(p).replace('"jobTitle": "Psicóloga Clínica e Neuropsicóloga"','"jobTitle": "Psicóloga Clínica e Avaliadora Psicológica"');write(p,s)
p='nucleo/context_processors.py';s=read(p).replace('"Psicologia e Neuropsicologia para compreender a mente, "\n        "cuidar das emoções e construir novos caminhos."', '"Avaliações psicológicas, laudos, pareceres e relatórios. "\n        "Psicoterapia com responsabilidade e acolhimento."');write(p,s)
p='templates/componentes/menu_principal.html';s=read(p)
# Marca apenas a URL exata como página atual, incluindo os itens do submenu.
s=re.sub(r'<a class="site-nav__link" href="([^"]+)" {% if (.*?) %}aria-current="page"{% endif %}>',r'<a class="site-nav__link {% if \2 %}site-nav__link--ativo{% endif %}" href="\1" {% if \2 %}aria-current="page"{% endif %}>',s)
for slug in ['burnout','cirurgia-bariatrica','esterilizacao','ansiedade-depressao','processos-judiciais','inss']:
    token='href="{% url \'servicos:avaliacao_especifica\' slug=\''+slug+'\' %}"'
    s=s.replace(token, token+" {% if request.path == '/servicos/avaliacao/"+slug+"/' %}aria-current=\"page\"{% endif %}")
s=s.replace('href="{% url \'servicos:avaliacao\' %}"','href="{% url \'servicos:avaliacao\' %}" {% if request.path == \'/servicos/avaliacao/\' %}aria-current="page"{% endif %}')
write(p,s)
p='templates/componentes/footer.html';s=read(p).replace('                        <li><a href="{% url \'servicos:avaliacao\' %}">Avaliações Especializadas</a></li>','');write(p,s)
# Contextualiza o legado sem produzir uma página órfã.
p='templates/servicos/avaliacao_hub.html';s=read(p).replace('Para outras necessidades, conheça também a ', 'Conheça também a <a href="{% url \'servicos:avaliacao_psicologica\' %}">visão geral da avaliação psicológica</a>, a ');write(p,s)
# Imagem social existente estava ausente no repositório; usa a nova fotografia temática.
p='templates/base/base.html';s=read(p).replace('/static/img/identidade/og_padrao.jpg','/static/img/avaliacoes/inss.webp');write(p,s)
# Adequação das expectativas editoriais antigas, preservando os testes funcionais.
p='conteudos/tests.py';s=read(p).replace('Conteúdos para apoiar sua reflexão','Informação que ajuda');write(p,s)
p='nucleo/tests_performance.py';s=read(p)
a=s.index('    def test_home_query_count_limite');b=s.index('    def ',a+8)
s=s[:a]+s[a:b].replace('6 queries','5 queries').replace('assertNumQueries(6)','assertNumQueries(5)')+s[b:]
s=s.replace("""        self.assertIn('class="placeholder-imagem placeholder-imagem--hero"', html)""","""        self.assertIn('class="editorial-retrato__vazio"', html)
        self.profissional.foto_principal = 'profissionais/retrato-teste.jpg'
        self.profissional.save(update_fields=['foto_principal'])
        html = self.client.get(reverse('paginas:inicio')).content.decode('utf-8')
        self.assertIn('loading="eager" fetchpriority="high"', html)""")
write(p,s)
p='nucleo/tests_regressao.py';s=read(p);a=s.index('    def test_home_queries_constantes');b=s.index('\nclass ',a);s=s[:a]+s[a:b].replace('assertNumQueries(6)','assertNumQueries(5)')+s[b:];write(p,s)
p='paginas/tests.py';s=read(p)
def method(text,name,body):
    pat=r'    def '+name+r'\(self\):.*?(?=\n    def |\nclass |\Z)'
    return re.sub(pat,'    def '+name+'(self):\n'+body+'\n',text,flags=re.S)
s=s.replace('Você não precisa permanecer preso ao que viveu.','Psicóloga Clínica e <em>Avaliadora Psicológica</em>')
s=s.replace("self.assertContains(response, 'Prazer, eu sou Mari Menezes.')","self.assertContains(response, 'Prazer, eu sou <em>Mari Menezes.</em>')")
s=s.replace("        self.assertContains(response, 'Meu propósito é ajudar pessoas')","        self.assertContains(response, 'escuta, investigação e cuidado')")
s=s.replace('Psicóloga, palestrante e facilitadora de grupos\')','Psicóloga Clínica e Avaliadora Psicológica\')')
s=method(s,'test_cards_identificacao_sem_diagnostico',"""        response = self.client.get(reverse('paginas:inicio'))
        for slug in ['burnout', 'cirurgia-bariatrica', 'esterilizacao', 'inss', 'processos-judiciais', 'ansiedade-depressao']:
            self.assertContains(response, '/servicos/avaliacao/' + slug + '/')
        self.assertNotContains(response, 'Você tem depressão')
        self.assertNotContains(response, 'aprovação garantida')""")
s=method(s,'test_etapas_atendimento_01_a_04',"""        response = self.client.get(reverse('paginas:inicio'))
        for etapa in ['Entender a demanda', 'Planejar a avaliação', 'Investigar com cuidado', 'Devolver e orientar']:
            self.assertContains(response, etapa)""")
s=method(s,'test_bloco_neuropsicologia_e_avaliacao',"""        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'Avaliações Psicológicas, Laudos e Pareceres')
        self.assertContains(response, 'Responsabilidade Técnica e Ética')
        html = response.content.decode('utf-8')
        self.assertLess(html.index('id="avaliacoes"'), html.index('id="atendimento"'))
        self.assertContains(response, '/servicos/neuropsicologia/')""")
s=s.replace('Como funciona o primeiro contato?','Como solicitar uma avaliação psicológica?').replace('Psicologia e Neuropsicologia são a mesma coisa?','Toda avaliação resulta em laudo?').replace('Como funciona uma avaliação neuropsicológica?','O atendimento pode ser online?')
s=method(s,'test_home_assets_carregados',"""        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'css/editorial.css')
        self.assertContains(response, 'js/navegacao.js')
        self.assertContains(response, 'img/avaliacoes/burnout.webp')""")
write(p,s)
p='servicos/tests.py';s=read(p)
a=s.index('    def test_psicologia_status_200');b=s.index('    # --- TRAUMAS',a)
seg=s[a:b].replace('css/paginas_internas.css','css/editorial.css').replace('<h1 class="hero-interno__titulo">Psicologia e Psicoterapia</h1>','<h1>Psicoterapia Humanizada para Promoção da Saúde Mental e Qualidade de Vida</h1>').replace('Um espaço de escuta profissional para compreender emoções, pensamentos, comportamentos e relações.','Você não precisa ter todas as respostas para começar.').replace("'Autoestima'","'autoestima'").replace("'Separação e Términos'","'Separação e recomeços'").replace("'Perdas e Luto'","'perdas, mudanças'").replace("'Recursos Emocionais'","'desenvolvimento pessoal'")
s=s[:a]+seg+s[b:]
s=s.replace('<h1 class="hero-interno__titulo">Avaliação Psicológica e Neuropsicológica</h1>','Avaliações Psicológicas,<br><em>Laudos e Pareceres</em>').replace("'processos técnicos distintos'","'Cada documento tem'")
s=method(s,'test_estados_ativos_navegacao_eixo_tecnico',"""        for path in ['/servicos/avaliacao/', '/servicos/avaliacao/burnout/', '/servicos/avaliacao/inss/']:
            response = self.client.get(path)
            self.assertContains(response, 'href="' + path + '" aria-current="page"')
        for path in ['/servicos/neuropsicologia/', '/servicos/reabilitacao-neurocognitiva/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'site-nav__dropdown')""")
write(p,s)
# Inclui as novas rotas nos testes existentes de SEO, links, H1 e acessibilidade de imagens.
p='nucleo/tests_seo_editorial.py';s=read(p).replace("        cls.urls_publicas = [","        cls.urls_publicas = [\n            '/credenciamento/',\n            *['/servicos/avaliacao/' + slug + '/' for slug in ['burnout', 'cirurgia-bariatrica', 'esterilizacao', 'inss', 'processos-judiciais', 'ansiedade-depressao']],")
write(p,s)
print('Ajustes de apresentação, SEO e testes editoriais concluídos.')

