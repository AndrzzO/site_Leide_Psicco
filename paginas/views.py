"""Views do app paginas."""
from django.shortcuts import render
from django.conf import settings
from django.http import Http404


from nucleo.models import Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import Artigo


def home(request):
    from servicos.editorial import AVALIACOES, FAQ_AVALIACAO, ETAPAS_AVALIACAO
    profissional = Profissional.objects.filter(ativo=True).first()
    return render(request, 'paginas/home.html', {
        'profissional': profissional,
        'avaliacoes': AVALIACOES,
        'faq_itens': FAQ_AVALIACAO,
        'etapas_avaliacao': ETAPAS_AVALIACAO,
        'artigos_publicados': Artigo.objects.publicados().select_related('categoria')[:3],
        'titulo_pagina': 'Avaliações, Laudos e Pareceres | Instituto Mente em Foco',
        'meta_descricao': 'Avaliações psicológicas, laudos, pareceres e relatórios com Mari Menezes. Psicoterapia para adolescentes e adultos. Atendimento online e presencial.',
    })


def credenciamento(request):
    from contato.forms import ContatoForm
    return render(request, 'paginas/credenciamento.html', {
        'titulo_pagina': 'Seja um Psicólogo Credenciado | Instituto Mente em Foco',
        'meta_descricao': 'Conheça a proposta de credenciamento de psicólogos do Instituto Mente em Foco. Registre interesse e esclareça critérios e possibilidades de atuação.',
        'form': ContatoForm(initial={'mensagem': 'Tenho interesse no credenciamento de psicólogos. '}),
    })


def inicio_temporario(request):
    """Fallback mantido para compatibilidade."""
    return home(request)


def sobre_mim(request):
    """
    Página institucional de apresentação da Psicóloga Mari Menezes.
    Consome o model Profissional de forma segura com fallbacks oficiais.
    """
    profissional = Profissional.objects.filter(ativo=True).first()

    # Áreas de atuação para o bloco de conexão clínica
    areas_relacionadas = AreaAtuacao.objects.filter(
        ativo=True
    ).order_by('ordem')[:3]

    itens_relacionados = [
        {
            'categoria': 'Área de Atuação',
            'titulo': area.titulo or area.nome,
            'resumo': area.resumo,
            'url': f"/servicos/{area.slug}/" if area.slug != 'novos-relacionamentos' else "/servicos/novos-relacionamentos/",
            'link_texto': 'Conhecer atendimento',
        }
        for area in areas_relacionadas
    ]

    imagem_url = ''
    if profissional:
        if profissional.foto_sobre:
            imagem_url = profissional.foto_sobre.url
        elif profissional.foto_principal:
            imagem_url = profissional.foto_principal.url

    breadcrumb = [
        {'titulo': 'Sobre Mim', 'url': None},
    ]

    contexto = {
        'profissional': profissional,
        'imagem_url': imagem_url,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Sobre Mim | Psicóloga Mari Menezes | Instituto Mente em Foco',
        'meta_descricao': (
            'Conheça a trajetória, visão clínica e propósito profissional da '
            'Psicóloga Mari Menezes no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'paginas/sobre_mim.html', contexto)


def politica_privacidade(request):
    """
    Aviso e Política de Privacidade do Instituto Mente em Foco.
    Apresenta de forma clara e factual o tratamento de dados do formulário de contato,
    assegurando conformidade com a LGPD até a consolidação jurídica no Prompt 11.
    """
    breadcrumb = [
        {'titulo': 'Política de Privacidade', 'url': ''}
    ]
    contexto = {
        'titulo_pagina': 'Política de Privacidade | Instituto Mente em Foco',
        'meta_descricao': (
            'Diretrizes de privacidade e tratamento de dados pessoais do Instituto Mente em Foco. '
            'Coleta mínima restrita ao retorno de mensagens institucionais.'
        ),
        'breadcrumb': breadcrumb,
        'canonical_path': '/politica-de-privacidade/',
        'meta_robots': 'noindex, follow',
    }
    return render(request, 'paginas/politica_privacidade.html', contexto)


def politica_cookies(request):
    """
    Política de Cookies e Tecnologias de Armazenamento do Instituto Mente em Foco.
    Apresenta de forma transparente os cookies estritamente necessários utilizados
    pela plataforma e atesta a ausência de rastreadores, pixels ou cookies de marketing.
    """
    breadcrumb = [
        {'titulo': 'Política de Cookies', 'url': ''}
    ]
    contexto = {
        'titulo_pagina': 'Política de Cookies | Instituto Mente em Foco',
        'meta_descricao': (
            'Transparência sobre cookies e armazenamento técnico no site do Instituto Mente em Foco. '
            'Utilização restrita a cookies estritamente necessários para segurança e funcionamento.'
        ),
        'breadcrumb': breadcrumb,
        'canonical_path': '/politica-de-cookies/',
        'meta_robots': 'noindex, follow',
    }
    return render(request, 'paginas/politica_cookies.html', contexto)



def laboratorio_design_system(request):
    """
    Página interna de desenvolvimento para validação visual, responsiva
    e acessível do Design System do Instituto Mente em Foco.
    Disponível estritamente quando DEBUG=True.
    Em produção, levanta Http404.
    """
    if not settings.DEBUG:
        raise Http404("Página não encontrada.")

    contexto = {
        'titulo_pagina': 'Design System — Laboratório Visual',
    }
    return render(request, 'paginas/laboratorio_design_system.html', contexto)
