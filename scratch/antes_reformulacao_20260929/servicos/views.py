from django.shortcuts import render
from .models import AreaAtuacao, Servico


def neuropsicologia(request):
    """
    Página de Neuropsicologia Clínica.
    Investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento.
    """
    servico = Servico.objects.filter(slug='neuropsicologia-clinica', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='neuropsicologia', ativo=True).first()

    aspectos_cognitivos = [
        {
            'icone': 'foco',
            'titulo': 'Atenção',
            'descricao': 'Sustentação do foco, alternância e filtragem de estímulos no cotidiano.',
        },
        {
            'icone': 'livro',
            'titulo': 'Memória',
            'descricao': 'Capacidade de retenção, consolidação e evocação de experiências e conhecimentos.',
        },
        {
            'icone': 'engrenagem',
            'titulo': 'Funções Executivas',
            'descricao': 'Planejamento, tomada de decisões, flexibilidade mental e regulação de ações.',
        },
        {
            'icone': 'lampada',
            'titulo': 'Raciocínio',
            'descricao': 'Processamento lógico, capacidade de abstração e resolução de problemas.',
        },
        {
            'icone': 'conversa',
            'titulo': 'Linguagem',
            'descricao': 'Compreensão, expressão verbal, fluência comunicativa e escrita.',
        },
        {
            'icone': 'coracao',
            'titulo': 'Aspectos Emocionais',
            'descricao': 'Integração entre dinâmicas afetivas e repercussões no humor e bem-estar.',
        },
        {
            'icone': 'usuario',
            'titulo': 'Comportamento',
            'descricao': 'Padrões de resposta e adaptação frente às demandas contextuais.',
        },
        {
            'icone': 'cerebro',
            'titulo': 'Funcionamento Cognitivo',
            'descricao': 'Perfil global de desempenho cognitivo e sua organização no dia a dia.',
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Investigação Clínica',
            'titulo': 'Avaliação Neuropsicológica',
            'resumo': 'Mapeamento detalhado do perfil cognitivo e funcional com base em instrumentos regulamentados.',
            'url': '/servicos/avaliacao-neuropsicologica/',
            'link_texto': 'Conhecer avaliação',
        },
        {
            'categoria': 'Acompanhamento',
            'titulo': 'Reabilitação Neurocognitiva',
            'resumo': 'Estratégias individualizadas voltadas ao funcionamento cognitivo no cotidiano, quando indicado.',
            'url': '/servicos/reabilitacao-neurocognitiva/',
            'link_texto': 'Conhecer reabilitação',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer psicoterapia',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Neuropsicologia', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'aspectos_cognitivos': aspectos_cognitivos,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Neuropsicologia | Instituto Mente em Foco',
        'meta_descricao': (
            'Investigação das relações entre funcionamento cerebral, cognição, '
            'emoções e comportamento no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/neuropsicologia.html', contexto)


def psicologia(request):
    """
    Página de Psicologia Clínica e Psicoterapia Individual.
    Apresenta temas trabalhados de forma ética, sem diagnósticos invasivos.
    """
    servico = Servico.objects.filter(slug='psicologia-clinica', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='psicologia', ativo=True).first()

    temas = [
        {
            'titulo': 'Ansiedade',
            'descricao': 'Compreensão das sensações de apreensão, preocupação excessiva e seus impactos na rotina.',
        },
        {
            'titulo': 'Autoestima',
            'descricao': 'Reconhecimento do próprio valor e fortalecimento da autoconfiança de forma gentil.',
        },
        {
            'titulo': 'Relacionamentos',
            'descricao': 'Acolhimento de impasses e dinâmicas na convivência afetiva, familiar ou social.',
        },
        {
            'titulo': 'Separação e Términos',
            'descricao': 'Elaboração das perdas, do encerramento de ciclos e da reorganização pessoal.',
        },
        {
            'titulo': 'Perdas e Luto',
            'descricao': 'Espaço seguro para acolher ausências e ressignificar a dor do luto no seu tempo.',
        },
        {
            'titulo': 'Mudanças de Vida',
            'descricao': 'Suporte emocional para transições importantes e novas etapas da vida pessoal ou profissional.',
        },
        {
            'titulo': 'Dificuldades Emocionais',
            'descricao': 'Acolhimento do mal-estar, do cansaço mental e dos momentos de sobrecarga.',
        },
        {
            'titulo': 'Conflitos Interpessoais',
            'descricao': 'Desenvolvimento de clareza na comunicação e resolução de divergências relacionais.',
        },
        {
            'titulo': 'Padrões de Relacionamento',
            'descricao': 'Identificação de repetições e busca de novas formas mais saudáveis de conviver.',
        },
        {
            'titulo': 'Experiências Difíceis',
            'descricao': 'Integração de vivências dolorosas do passado sem que elas dominem o presente.',
        },
        {
            'titulo': 'Recursos Emocionais',
            'descricao': 'Construção contínua de estratégias internas para lidar com os desafios cotidianos.',
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Acolhimento',
            'titulo': 'Traumas e Experiências Difíceis',
            'resumo': 'Quando uma experiência termina, suas marcas podem permanecer. Cuidado ético e respeitoso.',
            'url': '/servicos/traumas/',
            'link_texto': 'Conhecer atendimento',
        },
        {
            'categoria': 'Reorganização',
            'titulo': 'Separação e Recomeços',
            'resumo': 'Separar-se também é reorganizar a própria vida emocional e reencontrar a própria identidade.',
            'url': '/servicos/separacao-e-recomecos/',
            'link_texto': 'Conhecer atendimento',
        },
        {
            'categoria': 'Avaliação',
            'titulo': 'Avaliação Psicológica',
            'resumo': 'Processo estruturado de compreensão técnica de aspectos emocionais e comportamentais.',
            'url': '/servicos/avaliacao/',
            'link_texto': 'Saber mais',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Áreas de Atuação', 'url': '/#areas'},
        {'titulo': 'Psicologia', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'temas': temas,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Psicologia e Psicoterapia | Instituto Mente em Foco',
        'meta_descricao': (
            'Espaço de escuta profissional para compreender emoções, pensamentos, '
            'comportamentos e relações com acolhimento e sigilo profissional.'
        ),
    }
    return render(request, 'servicos/psicologia.html', contexto)


def traumas(request):
    """
    Página de Traumas e Experiências Difíceis.
    Comunicação serena e acolhedora sem promessa de cura ou sensacionalismo.
    """
    servico = Servico.objects.filter(slug='acompanhamento-traumas', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='traumas', ativo=True).first()

    repercussoes = [
        {
            'icone': 'coracao',
            'titulo': 'Emoções',
            'descricao': 'Sentimentos de vulnerabilidade, tristeza, medo, angústia ou oscilações de humor persistentes.',
        },
        {
            'icone': 'cerebro',
            'titulo': 'Pensamentos',
            'descricao': 'Hipervigilância, dúvidas frequentes sobre si ou lembranças involuntárias da experiência vivida.',
        },
        {
            'icone': 'folha',
            'titulo': 'Comportamentos',
            'descricao': 'Esquiva de lugares ou pessoas, alterações no padrão de sono e tendência ao isolamento defensivo.',
        },
        {
            'icone': 'escudo',
            'titulo': 'Relações',
            'descricao': 'Dificuldade para confiar novamente, receio da proximidade afetiva e sentimentos de incompreensão.',
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer atendimento',
        },
        {
            'categoria': 'Reorganização',
            'titulo': 'Separação e Recomeços',
            'resumo': 'Separar-se também é reorganizar a própria vida e reencontrar a própria identidade.',
            'url': '/servicos/separacao-e-recomecos/',
            'link_texto': 'Conhecer atendimento',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Áreas de Atuação', 'url': '/#areas'},
        {'titulo': 'Traumas', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'repercussoes': repercussoes,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Traumas e Experiências Difíceis | Instituto Mente em Foco',
        'meta_descricao': (
            'Quando uma experiência termina, suas marcas podem permanecer. '
            'Acompanhamento psicológico respeitoso no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/traumas.html', contexto)


def separacao_recomecos(request):
    """
    Página de Apoio em Separação e Recomeços.
    Abordagem de reorganização pessoal sem vitimização ou teorias não comprovadas.
    """
    servico = Servico.objects.filter(slug='atendimento-separacao', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='separacao-e-recomecos', ativo=True).first()

    aspectos = [
        {
            'numero': '01',
            'titulo': 'A Rotina',
            'texto': 'Reorganização de horários, tarefas diárias, ambiente e a adaptação a um novo cotidiano.',
        },
        {
            'numero': '02',
            'titulo': 'Sentimentos Contraditórios',
            'texto': 'Acolhimento da mistura de sentimentos: alívio, tristeza, raiva, incerteza e saudade.',
        },
        {
            'numero': '03',
            'titulo': 'Autoestima',
            'texto': 'Resgate do sentimento de valor próprio e superação de cobranças internas excessivas.',
        },
        {
            'numero': '04',
            'titulo': 'Projetos Pessoais',
            'texto': 'Revisão de planos futuros e construção de metas que façam sentido individualmente.',
        },
        {
            'numero': '05',
            'titulo': 'A Solidão',
            'texto': 'Compreensão do espaço individual, transformando o vazio em autodescoberta e solitude.',
        },
        {
            'numero': '06',
            'titulo': 'Limites Saudáveis',
            'texto': 'Definição de fronteiras claras na comunicação e nas decisões com o(a) ex-parceiro(a).',
        },
        {
            'numero': '07',
            'titulo': 'Reconstrução da Identidade',
            'texto': 'Reencontro com quem você é além da relação que terminou.',
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Continuidade',
            'titulo': 'Novos Relacionamentos',
            'resumo': 'Recomeçar não significa esquecer. Compreensão de escolhas, expectativas e limites.',
            'url': '/servicos/novos-relacionamentos/',
            'link_texto': 'Conhecer atendimento',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer atendimento',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Áreas de Atuação', 'url': '/#areas'},
        {'titulo': 'Separação & Recomeços', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'aspectos': aspectos,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Separação e Recomeços | Instituto Mente em Foco',
        'meta_descricao': (
            'Separar-se também é reorganizar a própria vida. Acompanhamento emocional '
            'para reconstrução pessoal e fortalecimento de recursos internos.'
        ),
    }
    return render(request, 'servicos/separacao_recomecos.html', contexto)


def novos_relacionamentos(request):
    """
    Página de Novos Relacionamentos.
    Foco na reflexão sobre escolhas, limites e convivência após términos.
    """
    servico = Servico.objects.filter(slug='novos-relacionamentos-atendimento', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='novos-relacionamentos', ativo=True).first()

    eixos = [
        {
            'classe': 'card-eixo--vontade',
            'badge': 'O Desejo',
            'titulo': 'Vontade de se envolver novamente',
            'texto': (
                'O anseio legítimo por afeto, parceria e cumplicidade. A vontade de compartilhar '
                'momentos e viver novas histórias com alguém especial.'
            ),
        },
        {
            'classe': 'card-eixo--cautela',
            'badge': 'A Defesa',
            'titulo': 'O medo de sofrer novamente',
            'texto': (
                'A cautela natural nascida de decepções passadas. Dúvidas sobre confiar, '
                'receio de reviver dores antigas ou repetir dinâmicas que machucaram.'
            ),
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Reorganização',
            'titulo': 'Separação e Recomeços',
            'resumo': 'Separar-se também é reorganizar a própria vida e reencontrar a própria identidade.',
            'url': '/servicos/separacao-e-recomecos/',
            'link_texto': 'Conhecer atendimento',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer atendimento',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Áreas de Atuação', 'url': '/#areas'},
        {'titulo': 'Novos Relacionamentos', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'eixos': eixos,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Novos Relacionamentos | Instituto Mente em Foco',
        'meta_descricao': (
            'Recomeçar não significa esquecer. Compreenda suas experiências passadas, '
            'fortaleça seus limites e construa novas possibilidades relacionais.'
        ),
    }
    return render(request, 'servicos/novos_relacionamentos.html', contexto)


def avaliacao(request):
    """
    Página Hub de Avaliação Psicológica e Neuropsicológica.
    Apresenta e diferencia com clareza as duas modalidades técnicas,
    demonstrando como podem se complementar conforme a demanda individual.
    """
    servico_psico = Servico.objects.filter(slug='avaliacao-psicologica', ativo=True).first()
    servico_neuro = Servico.objects.filter(slug='avaliacao-neuropsicologica', ativo=True).first()
    area_neuro = AreaAtuacao.objects.filter(slug='neuropsicologia', ativo=True).first()

    itens_relacionados = [
        {
            'categoria': 'Área Clínica',
            'titulo': 'Neuropsicologia Clínica',
            'resumo': 'Investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento.',
            'url': '/servicos/neuropsicologia/',
            'link_texto': 'Conhecer neuropsicologia',
        },
        {
            'categoria': 'Acompanhamento',
            'titulo': 'Reabilitação Neurocognitiva',
            'resumo': 'Estratégias individualizadas voltadas ao funcionamento cognitivo no cotidiano, quando indicado.',
            'url': '/servicos/reabilitacao-neurocognitiva/',
            'link_texto': 'Conhecer reabilitação',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer psicoterapia',
        },
    ]

    breadcrumb = [
        {'titulo': 'Avaliação', 'url': None},
    ]

    contexto = {
        'servico_psico': servico_psico,
        'servico_neuro': servico_neuro,
        'area_neuro': area_neuro,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Avaliação Psicológica e Neuropsicológica | Instituto Mente em Foco',
        'meta_descricao': (
            'Processos técnicos e éticos de Avaliação Psicológica e Avaliação Neuropsicológica '
            'conduzidos com rigor e acolhimento no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/avaliacao_hub.html', contexto)


def avaliacao_psicologica(request):
    """
    Página Dedicada de Avaliação Psicológica.
    Investigação estruturada de aspectos emocionais, de personalidade e comportamento.
    """
    servico = Servico.objects.filter(slug='avaliacao-psicologica', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='psicologia', ativo=True).first()

    itens_relacionados = [
        {
            'categoria': 'Investigação Clínica',
            'titulo': 'Avaliação Neuropsicológica',
            'resumo': 'Mapeamento detalhado do perfil cognitivo e funcional com base em instrumentos regulamentados.',
            'url': '/servicos/avaliacao-neuropsicologica/',
            'link_texto': 'Conhecer avaliação',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer psicoterapia',
        },
        {
            'categoria': 'Hub Institucional',
            'titulo': 'Visão Geral das Avaliações',
            'resumo': 'Entenda a distinção e complementaridade entre os processos avaliativos.',
            'url': '/servicos/avaliacao/',
            'link_texto': 'Ver página hub',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Avaliação', 'url': '/servicos/avaliacao/'},
        {'titulo': 'Avaliação Psicológica', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Avaliação Psicológica | Instituto Mente em Foco',
        'meta_descricao': (
            'Processo técnico estruturado para compreensão de aspectos emocionais '
            'e comportamentais no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/avaliacao_psicologica.html', contexto)


def avaliacao_neuropsicologica(request):
    """
    Página Dedicada de Avaliação Neuropsicológica.
    Investigação minuciosa do perfil cognitivo e funcional no contexto da Neuropsicologia.
    """
    servico = Servico.objects.filter(slug='avaliacao-neuropsicologica', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='neuropsicologia', ativo=True).first()

    aspectos_investigados = [
        {
            'titulo': 'Atenção e Concentração',
            'descricao': 'Capacidade de direcionamento, sustentação e alternância do foco mental.',
        },
        {
            'titulo': 'Memória e Aprendizagem',
            'descricao': 'Retenção e evocação de informações verbais e visuais no tempo.',
        },
        {
            'titulo': 'Funções Executivas',
            'descricao': 'Capacidade de planejamento, organização, tomada de decisão e autorregulação.',
        },
        {
            'titulo': 'Raciocínio e Resolução de Problemas',
            'descricao': 'Processamento lógico, abstração conceitual e flexibilidade cognitiva.',
        },
        {
            'titulo': 'Linguagem e Comunicação',
            'descricao': 'Fluência verbal, compreensão, nomeação e expressão.',
        },
        {
            'titulo': 'Aspectos Emocionais e Comportamentais',
            'descricao': 'Integração entre o funcionamento cognitivo e as repercussões cotidianas.',
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Acompanhamento',
            'titulo': 'Reabilitação Neurocognitiva',
            'resumo': 'Estratégias individualizadas voltadas ao funcionamento cognitivo no cotidiano, quando indicado.',
            'url': '/servicos/reabilitacao-neurocognitiva/',
            'link_texto': 'Conhecer reabilitação',
        },
        {
            'categoria': 'Área Clínica',
            'titulo': 'Neuropsicologia Clínica',
            'resumo': 'Investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento.',
            'url': '/servicos/neuropsicologia/',
            'link_texto': 'Conhecer neuropsicologia',
        },
        {
            'categoria': 'Investigação Clínica',
            'titulo': 'Avaliação Psicológica',
            'resumo': 'Compreensão de aspectos emocionais, dinâmica de personalidade e comportamento.',
            'url': '/servicos/avaliacao-psicologica/',
            'link_texto': 'Conhecer avaliação',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Avaliação', 'url': '/servicos/avaliacao/'},
        {'titulo': 'Avaliação Neuropsicológica', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'aspectos_investigados': aspectos_investigados,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Avaliação Neuropsicológica | Instituto Mente em Foco',
        'meta_descricao': (
            'Investigação do perfil cognitivo e funcional por meio de instrumentos padronizados '
            'e devolutiva técnica no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/avaliacao_neuropsicologica.html', contexto)


def reabilitacao_neurocognitiva(request):
    """
    Página de Reabilitação Neurocognitiva.
    Após avaliação e quando houver indicação, estratégias individualizadas no cotidiano.
    """
    servico = Servico.objects.filter(slug='reabilitacao-neurocognitiva', ativo=True).first()
    area = AreaAtuacao.objects.filter(slug='neuropsicologia', ativo=True).first()

    eixos_reabilitacao = [
        {
            'icone': 'cerebro',
            'titulo': 'Funcionamento Cognitivo',
            'descricao': (
                'Desenvolvimento, estimulação e adaptação de recursos cognitivos, '
                'com foco nas habilidades preservadas e na construção de compensações práticas.'
            ),
        },
        {
            'icone': 'sol',
            'titulo': 'Vida Cotidiana',
            'descricao': (
                'Aplicação direta e funcional das estratégias na rotina diária, no ambiente de trabalho '
                'ou estudos, favorecendo a autonomia e o bem-estar.'
            ),
        },
        {
            'icone': 'coracao',
            'titulo': 'Necessidades e Objetivos da Pessoa',
            'descricao': (
                'Planejamento centrado na história única de cada indivíduo, respeitando seus limites, '
                'suas prioridades pessoais e seu contexto de convivência.'
            ),
        },
    ]

    itens_relacionados = [
        {
            'categoria': 'Investigação Prévia',
            'titulo': 'Avaliação Neuropsicológica',
            'resumo': 'Mapeamento minucioso do perfil cognitivo e funcional que orienta a indicação.',
            'url': '/servicos/avaliacao-neuropsicologica/',
            'link_texto': 'Conhecer avaliação',
        },
        {
            'categoria': 'Área Clínica',
            'titulo': 'Neuropsicologia Clínica',
            'resumo': 'Investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento.',
            'url': '/servicos/neuropsicologia/',
            'link_texto': 'Conhecer neuropsicologia',
        },
        {
            'categoria': 'Psicoterapia',
            'titulo': 'Psicologia Clínica',
            'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos e relações.',
            'url': '/servicos/psicologia/',
            'link_texto': 'Conhecer psicoterapia',
        },
    ]

    imagem_url = ''
    if servico and servico.imagem_principal:
        imagem_url = servico.imagem_principal.url
    elif area and area.imagem:
        imagem_url = area.imagem.url

    breadcrumb = [
        {'titulo': 'Neuropsicologia', 'url': '/servicos/neuropsicologia/'},
        {'titulo': 'Reabilitação Neurocognitiva', 'url': None},
    ]

    contexto = {
        'servico': servico,
        'area': area,
        'imagem_url': imagem_url,
        'eixos_reabilitacao': eixos_reabilitacao,
        'breadcrumb': breadcrumb,
        'itens_relacionados': itens_relacionados,
        'titulo_pagina': 'Reabilitação Neurocognitiva | Instituto Mente em Foco',
        'meta_descricao': (
            'Após avaliação e quando houver indicação, estratégias individualizadas voltadas '
            'ao funcionamento cognitivo e à vida cotidiana no Instituto Mente em Foco.'
        ),
    }
    return render(request, 'servicos/reabilitacao_neurocognitiva.html', contexto)
