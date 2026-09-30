"""Views do app paginas."""
from django.shortcuts import render
from django.conf import settings
from django.http import Http404


from nucleo.models import Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import Artigo


def home(request):
    """
    Renderiza a Home oficial e completa do Instituto Mente em Foco.
    Consome dados dinâmicos do CMS (Profissional, AreaAtuacao, Servico)
    e disponibiliza conteúdos estruturados para as 11 seções da página.
    """
    # Profissional ativa
    profissional = Profissional.objects.filter(ativo=True).first()

    # Áreas de atuação para os cards fotográficos da Home
    areas_atuacao = AreaAtuacao.objects.filter(
        ativo=True,
        mostrar_na_home=True
    ).order_by('ordem', 'nome')

    # Serviços com destaque para a Home
    servicos_destaque = Servico.objects.filter(
        ativo=True,
        mostrar_na_home=True
    ).select_related('area').order_by('ordem', 'nome')

    # Cards de identificação oficiais (Prompt Seção 30)
    cards_identificacao = [
        {
            'icone': 'coracao',
            'frase': 'Meu relacionamento terminou, mas eu ainda não consegui seguir.',
        },
        {
            'icone': 'escudo',
            'frase': 'Tenho medo de me envolver novamente.',
        },
        {
            'icone': 'cadeado',
            'frase': 'Não consigo confiar como antes.',
        },
        {
            'icone': 'espiral',
            'frase': 'Sinto que estou repetindo os mesmos padrões.',
        },
        {
            'icone': 'sol',
            'frase': 'Comecei um novo relacionamento, mas o passado continua presente.',
        },
        {
            'icone': 'espelho',
            'frase': 'Depois de tudo que aconteceu, não sei mais quem eu sou.',
        },
        {
            'icone': 'folha',
            'frase': 'Estou emocionalmente cansado(a) e não sei por onde começar.',
        },
    ]

    # Processo de atendimento em 4 etapas (Prompt Seções 48-52)
    etapas_processo = [
        {
            'numero': '01',
            'titulo': 'Conversar',
            'descricao': 'A pessoa apresenta aquilo que está vivendo.',
        },
        {
            'numero': '02',
            'titulo': 'Compreender',
            'descricao': 'A demanda e a história são compreendidas.',
        },
        {
            'numero': '03',
            'titulo': 'Cuidar',
            'descricao': 'São construídas estratégias de acordo com as necessidades.',
        },
        {
            'numero': '04',
            'titulo': 'Reconstruir',
            'descricao': 'A pessoa desenvolve recursos para lidar com novos momentos e desafios.',
        },
    ]

    # Prévia de temas editoriais futuros para a seção Conteúdos (Prompt Seção 68)
    temas_conteudos = [
        {
            'categoria': 'Acolhimento',
            'tempo_leitura': '4 min de leitura',
            'titulo': 'Quando procurar ajuda psicológica?',
            'resumo': 'Reconhecer o momento de buscar apoio é um ato de coragem e autocuidado com a própria trajetória.',
        },
        {
            'categoria': 'Traumas',
            'tempo_leitura': '5 min de leitura',
            'titulo': 'Por que algumas experiências continuam doendo mesmo depois de anos?',
            'resumo': 'Compreenda como marcas emocionais não elaboradas reverberam no presente e como acolhê-las.',
        },
        {
            'categoria': 'Separação & Recomeço',
            'tempo_leitura': '6 min de leitura',
            'titulo': 'Como lidar emocionalmente com o fim de um relacionamento?',
            'resumo': 'O luto pelo término e o processo gradual de reencontro consigo mesmo antes de novos passos.',
        },
        {
            'categoria': 'Neuropsicologia',
            'tempo_leitura': '5 min de leitura',
            'titulo': 'O que é uma avaliação neuropsicológica e quando ela é indicada?',
            'resumo': 'Investigação pormenorizada das funções cognitivas e sua importância na rotina e intervenções.',
        },
    ]

    # Perguntas Frequentes oficiais (Prompt Seção 73)
    faq_itens = [
        {
            'pergunta': 'Como funciona o primeiro contato?',
            'resposta': 'O primeiro contato é um momento inicial de escuta para você apresentar suas dúvidas e necessidades. Nele alinhamos como o acompanhamento psicológico ou neuropsicológico pode apoiar sua história com respeito e sigilo.',
        },
        {
            'pergunta': 'Psicologia e Neuropsicologia são a mesma coisa?',
            'resposta': 'Não. A Psicologia clínica foca no acolhimento, na elaboração das dores emocionais, nos conflitos e nas relações humanas. A Neuropsicologia investiga detalhadamente a relação entre o cérebro e as funções cognitivas (como atenção, memória e raciocínio).',
        },
        {
            'pergunta': 'Como funciona uma avaliação neuropsicológica?',
            'resposta': 'É uma investigação clínica estruturada e minuciosa, conduzida por entrevistas e aplicação de instrumentos padronizados validados pelo Conselho Federal de Psicologia, com posterior laudo e devolutiva explicativa.',
        },
        {
            'pergunta': 'O que acontece na primeira sessão?',
            'resposta': 'Na primeira consulta, construímos um espaço seguro para que você possa falar livremente sobre o que motivou a busca por atendimento, alinhando expectativas e o plano terapêutico.',
        },
    ]

    # Artigos reais publicados (se houver, têm precedência sobre a prévia estática)
    artigos_publicados = Artigo.objects.publicados().select_related('categoria')[:3]

    contexto = {
        'profissional': profissional,
        'areas_atuacao': areas_atuacao,
        'servicos_destaque': servicos_destaque,
        'cards_identificacao': cards_identificacao,
        'etapas_processo': etapas_processo,
        'temas_conteudos': temas_conteudos,
        'artigos_publicados': artigos_publicados,
        'faq_itens': faq_itens,
    }
    return render(request, 'paginas/home.html', contexto)


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
