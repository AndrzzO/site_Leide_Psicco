from pathlib import Path
root = Path.cwd()
def read(p): return (root/p).read_text(encoding='utf-8-sig')
def write(p, text): (root/p).write_text(text,encoding='utf-8')
p='templates/base/base.html'
s=read(p).replace("    {% block extra_head %}", "    <link rel=\"stylesheet\" href=\"{% static 'css/editorial.css' %}\">\n    {% block extra_head %}")
write(p,s)
p='paginas/views.py'
s=read(p)
start=s.index('def home(request):')
end=s.index('\ndef inicio_temporario',start)
s=s[:start]+'''def home(request):
    from servicos.editorial import AVALIACOES, FAQ_AVALIACAO, ETAPAS_AVALIACAO
    profissional = Profissional.objects.filter(ativo=True).first()
    return render(request, 'paginas/home.html', {
        'profissional': profissional,
        'avaliacoes': AVALIACOES,
        'faq_itens': FAQ_AVALIACAO,
        'etapas_avaliacao': ETAPAS_AVALIACAO,
        'artigos_publicados': Artigo.objects.publicados().select_related('categoria')[:3],
        'titulo_pagina': 'Avaliações Psicológicas, Laudos e Pareceres | Mari Menezes',
        'meta_descricao': 'Avaliações psicológicas, laudos, pareceres e relatórios com Mari Menezes. Psicoterapia para adolescentes e adultos. Atendimento online e presencial.',
    })


def credenciamento(request):
    from contato.forms import ContatoForm
    return render(request, 'paginas/credenciamento.html', {
        'titulo_pagina': 'Seja um Psicólogo Credenciado | Instituto Mente em Foco',
        'meta_descricao': 'Conheça a proposta de credenciamento de psicólogos do Instituto Mente em Foco. Registre interesse e esclareça critérios e possibilidades de atuação.',
        'form': ContatoForm(initial={'mensagem': 'Tenho interesse no credenciamento de psicólogos. '}),
    })

''' + s[end:]
write(p,s)
p='paginas/urls.py';s=read(p).replace("    path('sobre-mim/'", "    path('credenciamento/', views.credenciamento, name='credenciamento'),\n    path('sobre-mim/'");write(p,s)
p='servicos/views.py';s=read(p)
start=s.index('def avaliacao(request):');end=s.index('\ndef avaliacao_psicologica',start)
s=s[:start]+'''def avaliacao(request):
    from .editorial import AVALIACOES, FAQ_AVALIACAO, ETAPAS_AVALIACAO
    return render(request, 'servicos/avaliacao_hub.html', {
        'avaliacoes': AVALIACOES, 'faq_itens': FAQ_AVALIACAO,
        'etapas_avaliacao': ETAPAS_AVALIACAO,
        'titulo_pagina': 'Avaliações Psicológicas, Laudos e Pareceres | Mente em Foco',
        'meta_descricao': 'Conheça avaliações para burnout, bariátrica, esterilização, INSS, processos judiciais, ansiedade e depressão. Entenda laudos, relatórios e pareceres.',
        'breadcrumb': [{'titulo': 'Avaliações Psicológicas', 'url': None}],
    })


def avaliacao_especifica(request, slug):
    from django.http import Http404
    from .editorial import AVALIACOES
    item = next((a for a in AVALIACOES if a['slug'] == slug), None)
    if item is None:
        raise Http404('Avaliação não encontrada.')
    return render(request, 'servicos/avaliacao_especifica.html', {
        'avaliacao': item, 'titulo_pagina': item['h1'] + ' | Mente em Foco',
        'meta_descricao': item['meta'],
        'etapas_avaliacao': item['processo'],
        'faq_itens': [{'pergunta': q, 'resposta': a} for q, a in item['faq']],
        'relacionados': [a for a in AVALIACOES if a['slug'] in item['relacionados']],
        'breadcrumb': [
            {'titulo': 'Avaliações Psicológicas', 'url': '/servicos/avaliacao/'},
            {'titulo': item['nome'], 'url': None},
        ],
    })

''' + s[end:]
s=s.replace("'titulo_pagina': 'Psicologia e Psicoterapia | Instituto Mente em Foco'", "'titulo_pagina': 'Psicoterapia Online e Presencial | Instituto Mente em Foco'")
write(p,s)
p='servicos/urls.py';s=read(p).replace("    path('avaliacao/',", "    path('avaliacao/<slug:slug>/', views.avaliacao_especifica, name='avaliacao_especifica'),\n    path('avaliacao/',");write(p,s)
# Reutiliza o formulário existente sem alterar o fluxo de validação ou persistência.
p='templates/contato/index.html';s=read(p)
start=s.index('                <form action=')
end=s.index('</form>',start)+len('</form>')
form=s[start:end]
form=form.replace("action=\"{% url 'contato:index' %}\"", "action=\"{{ form_action|default:'/contato/' }}\"")
form=form.replace('                    <!-- Serviço de Interesse -->', "                    {% if not ocultar_servico %}\n                    <!-- Serviço de Interesse -->")
form=form.replace('                    <!-- Mensagem Breve -->', "                    {% endif %}\n                    <!-- Mensagem Breve -->")
form=form.replace('<span>Enviar mensagem</span>',"<span>{{ botao_texto|default:'Enviar mensagem' }}</span>")
write('templates/componentes/formulario_contato.html',form)
s=s[:start]+"                {% include 'componentes/formulario_contato.html' %}"+s[end:]
s=s.replace('class="contato-formulario"', 'class="contato-formulario" id="formulario-contato"')
if 'id="formulario-contato"' not in s:
    s=s.replace('<!-- Formulário Seguro -->','<div id="formulario-contato"></div>\n                <!-- Formulário Seguro -->')
s=s.replace('Escolha o canal mais confortável para iniciar sua conversa.', 'Solicite uma avaliação psicológica, agende uma consulta ou converse sobre credenciamento.')
s=s.replace('Se preferir uma resposta rápida e direta, utilize nosso canal no WhatsApp.', 'Quando disponível, você também pode utilizar nosso canal no WhatsApp.')
write(p,s)
p='contato/views.py';s=read(p)
s=s.replace('        form = ContatoForm()','''        assuntos = {
            'avaliacao': 'Gostaria de solicitar uma avaliação psicológica.',
            'consulta': 'Gostaria de agendar uma consulta.',
            'psicoterapia': 'Gostaria de informações sobre psicoterapia.',
            'credenciamento': 'Tenho interesse no credenciamento de psicólogos.',
        }
        from servicos.editorial import AVALIACOES
        assuntos.update({a['slug']: 'Gostaria de informações sobre ' + a['h1'].lower() + '.' for a in AVALIACOES})
        mensagem_inicial = assuntos.get(request.GET.get('assunto', ''), '')
        form = ContatoForm(initial={'mensagem': mensagem_inicial})''')
s=s.replace("'acolhedor em Psicologia e Neuropsicologia com a Psicóloga Mari Menezes.'","'acolhedor em avaliações psicológicas e psicoterapia com Mari Menezes.'")
write(p,s)
p='nucleo/sitemaps.py';s=read(p)
s=s.replace("ItemPaginaEstatica('paginas:sobre_mim',", "ItemPaginaEstatica('paginas:credenciamento', 0.6, 'monthly'),\n            ItemPaginaEstatica('paginas:sobre_mim',")
s=s.replace("sitemaps = {",'''class AvaliacoesEspecificasSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        from servicos.editorial import AVALIACOES
        return [item['slug'] for item in AVALIACOES]

    def location(self, slug):
        return reverse('servicos:avaliacao_especifica', kwargs={'slug': slug})


sitemaps = {
    'avaliacoes_especificas': AvaliacoesEspecificasSitemap(),''')
write(p,s)
# Preserva o CMS e não faz alterações no banco.
p='templates/componentes/footer.html';s=read(p)
s=s.replace('{{ ASSINATURA_INSTITUCIONAL }}','Avaliações psicológicas, laudos, pareceres e relatórios. Psicoterapia com responsabilidade e acolhimento.')
s=s.replace('<li><a href="{% url \'servicos:psicologia\' %}">Psicologia Clínica</a></li>', '<li><a href="{% url \'servicos:avaliacao\' %}">Avaliações, Laudos e Pareceres</a></li>\n                        <li><a href="{% url \'servicos:psicologia\' %}">Psicoterapia</a></li>\n                        <li><a href="{% url \'paginas:credenciamento\' %}">Credenciamento de Psicólogos</a></li>')
write(p,s)
p='templates/paginas/sobre_mim.html';s=read(p)
s=s.replace('Psicóloga, palestrante e facilitadora de grupos, com atuação em Psicologia e Neuropsicologia.','Psicóloga Clínica e Avaliadora Psicológica. Avaliações, laudos, pareceres, relatórios e atendimento clínico para adolescentes e adultos.')
s=s.replace('Mari Menezes • Psicóloga & Neuropsicóloga','Mari Menezes • Psicóloga Clínica e Avaliadora')
s=s.replace('Um método de acolhimento que respeita','Uma prática de acolhimento que respeita')
write(p,s)
p='templates/servicos/avaliacao_psicologica.html';s=read(p)
# Adiciona navegação específica sem remover o conteúdo e a rota legados.
s=s.replace('{% block content %}', """{% block content %}
<section class="editorial-secao editorial-secao--areia"><div class="site-container"><span class="eyebrow">AVALIAÇÕES E DOCUMENTOS</span><h2>Encontre a avaliação para sua demanda</h2><p>Burnout, ansiedade e depressão, bariátrica, esterilização, INSS e processos judiciais: conheça finalidades, etapas e limites de cada atendimento.</p><a class="editorial-link" href="{% url 'servicos:avaliacao' %}">Conhecer todas as avaliações, laudos e pareceres ↗</a></div></section>""")
write(p,s)
p='static/js/navegacao.js';s=read(p)
s=s.replace("panel.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex=\"-1\"])')", "panel.querySelectorAll('a[href], summary, button:not([disabled]), [tabindex]:not([tabindex=\"-1\"])')")
s=s.replace("      // Inclui o botão de alternância", "      .filter((elemento) => elemento.getClientRects().length > 0);\n      // Inclui o botão de alternância") if False else s
s=s.replace('      );\n      // Inclui', '      ).filter((elemento) => elemento.getClientRects().length > 0);\n      // Inclui')
s += """
// Submenus nativos: Enter/Espaço, fechamento por Escape, clique fora e saída de foco.
document.querySelectorAll('.site-nav__dropdown').forEach((dropdown) => {
  dropdown.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && dropdown.open) {
      event.preventDefault();
      event.stopPropagation();
      dropdown.open = false;
      dropdown.querySelector('summary').focus();
    }
  });
  dropdown.addEventListener('focusout', () => {
    setTimeout(() => {
      if (!dropdown.contains(document.activeElement)) dropdown.open = false;
    }, 0);
  });
});
document.addEventListener('click', (event) => {
  document.querySelectorAll('.site-nav__dropdown[open]').forEach((dropdown) => {
    if (!dropdown.contains(event.target)) dropdown.open = false;
  });
});
"""
write(p,s)
print('Integração editorial concluída.')

