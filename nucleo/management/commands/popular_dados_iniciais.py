"""
Comando de gerenciamento para carregar dados institucionais iniciais de forma 100% idempotente.
Somente utiliza informações reais fornecidas pelo cliente e registradas na documentação oficial.
"""
from django.core.management.base import BaseCommand
from nucleo.models import ConfiguracaoSite, Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import CategoriaArtigo, Artigo


class Command(BaseCommand):
    help = 'Carrega dados institucionais iniciais e serviços aprovados de forma idempotente.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando carga de dados institucionais iniciais...'))

        # 1. Configuração Global do Site (Singleton)
        config, criada = ConfiguracaoSite.objects.get_or_create(
            pk=1,
            defaults={
                'nome_instituto': 'Instituto Mente em Foco',
                'slogan_principal': 'COMPREENDER • CUIDAR • RECONSTRUIR',
                'frase_institucional': (
                    'Psicologia e Neuropsicologia para compreender a mente, '
                    'cuidar das emoções e construir novos caminhos.'
                ),
                'frase_emocional': 'Sua história merece ser compreendida.',
                'cta_principal': 'Comece por você.',
                'mensagem_whatsapp_padrao': (
                    'Olá, Mari. Conheci o Instituto Mente em Foco pelo site e '
                    'gostaria de informações sobre o atendimento psicológico/neuropsicológico.'
                ),
                'ativo': True,
            }
        )
        status_config = 'Criada' if criada else 'Já existente'
        self.stdout.write(f'  [ConfiguracaoSite] {status_config}: {config.nome_instituto}')

        # 2. Profissional Principal (Mari Menezes)
        prof, criada = Profissional.objects.get_or_create(
            slug='mari-menezes',
            defaults={
                'nome': 'Mari Menezes',
                'nome_exibicao': 'Psicóloga Mari Menezes',
                'titulo_profissional': 'Psicóloga, palestrante e facilitadora de grupos',
                'atuacao_resumida': 'Psicologia e Neuropsicologia',
                'biografia_curta': (
                    'Minha prática parte da compreensão de que cada pessoa carrega '
                    'uma história que precisa ser compreendida antes de ser julgada. '
                    'Meu trabalho busca oferecer um espaço de escuta profissional, '
                    'acolhimento e construção de estratégias para diferentes momentos da vida.'
                ),
                'frase_destaque': (
                    'Meu propósito é ajudar pessoas a compreenderem melhor a própria '
                    'história e encontrarem recursos para seguir seus caminhos.'
                ),
                'ordem': 1,
                'ativo': True,
                'destaque': True,
            }
        )
        status_prof = 'Criada' if criada else 'Já existente'
        self.stdout.write(f'  [Profissional] {status_prof}: {prof.nome_exibicao}')

        # 3. Áreas de Atuação
        areas_dados = [
            {
                'nome': 'Psicologia',
                'slug': 'psicologia',
                'titulo': 'Psicologia',
                'resumo': 'Compreenda suas emoções, pensamentos e comportamentos.',
                'ordem': 1,
            },
            {
                'nome': 'Neuropsicologia',
                'slug': 'neuropsicologia',
                'titulo': 'Neuropsicologia',
                'resumo': 'Entenda a relação entre cérebro, cognição, emoções e comportamento.',
                'ordem': 2,
            },
            {
                'nome': 'Traumas',
                'slug': 'traumas',
                'titulo': 'Traumas',
                'resumo': 'Elabore experiências difíceis e desenvolva estratégias de enfrentamento.',
                'frase_destaque': 'Uma experiência difícil não precisa definir toda a sua história.',
                'ordem': 3,
            },
            {
                'nome': 'Separação e Recomeços',
                'slug': 'separacao-e-recomecos',
                'titulo': 'Separação e Recomeços',
                'resumo': 'Reconstrua sua vida emocional e fortaleça seus recursos.',
                'frase_destaque': 'Antes de escolher novamente alguém, talvez seja importante reencontrar você.',
                'ordem': 4,
            },
            {
                'nome': 'Novos Relacionamentos',
                'slug': 'novos-relacionamentos',
                'titulo': 'Novos Relacionamentos',
                'resumo': 'Compreenda seu passado, fortaleça seus limites e construa novas possibilidades.',
                'frase_destaque': 'Recomeçar não significa esquecer.',
                'ordem': 5,
            },
        ]

        areas_map = {}
        for dados in areas_dados:
            slug = dados['slug']
            area, criada = AreaAtuacao.objects.get_or_create(
                slug=slug,
                defaults=dados
            )
            areas_map[slug] = area
            status = 'Criada' if criada else 'Já existente'
            self.stdout.write(f'  [AreaAtuacao] {status}: {area.nome}')

        # 4. Serviços Clínicos e Avaliativos
        servicos_dados = [
            {
                'nome': 'Psicologia Clínica',
                'slug': 'psicologia-clinica',
                'area': areas_map.get('psicologia'),
                'titulo': 'Psicologia Clínica e Psicoterapia',
                'subtitulo': 'Um espaço de escuta profissional, acolhimento e compreensão',
                'resumo': 'Um espaço de escuta profissional para compreender emoções, pensamentos, comportamentos e relações.',
                'descricao': (
                    'A psicoterapia oferece um espaço ético e sigiloso para acolher '
                    'suas experiências emocionais, conflitos e momentos de mudança, '
                    'desenvolvendo recursos internos para novas possibilidades.'
                ),
                'icone': 'cerebro',
                'ordem': 1,
            },
            {
                'nome': 'Neuropsicologia Clínica',
                'slug': 'neuropsicologia-clinica',
                'area': areas_map.get('neuropsicologia'),
                'titulo': 'Neuropsicologia Clínica',
                'subtitulo': 'Compreendendo o funcionamento cognitivo e cerebral',
                'resumo': 'Investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento.',
                'descricao': (
                    'Atuação focada no entendimento detalhado de funções cognitivas '
                    '(como atenção, memória e raciocínio) e seu impacto prático na rotina diária.'
                ),
                'icone': 'perfil',
                'ordem': 2,
            },
            {
                'nome': 'Avaliação Psicológica',
                'slug': 'avaliacao-psicologica',
                'area': areas_map.get('psicologia'),
                'titulo': 'Avaliação Psicológica',
                'subtitulo': 'Investigação de aspectos emocionais e de personalidade',
                'resumo': 'Processo estruturado de compreensão de aspectos emocionais e comportamentais.',
                'descricao': (
                    'Processo técnico estruturado conduzido por entrevistas clínicas e instrumentos '
                    'validados, fornecendo devolutiva clara sobre a dinâmica emocional.'
                ),
                'icone': 'prancheta',
                'ordem': 3,
            },
            {
                'nome': 'Avaliação Neuropsicológica',
                'slug': 'avaliacao-neuropsicologica',
                'area': areas_map.get('neuropsicologia'),
                'titulo': 'Avaliação Neuropsicológica',
                'subtitulo': 'Mapeamento minucioso do perfil cognitivo',
                'resumo': 'Investigação pormenorizada de atenção, memória, linguagem e funções executivas.',
                'descricao': (
                    'Avaliação aprofundada com aplicação de testes padronizados para mapear '
                    'o funcionamento cognitivo, auxiliando no diagnóstico diferencial e em intervenções.'
                ),
                'icone': 'prancheta',
                'ordem': 4,
            },
            {
                'nome': 'Reabilitação Neurocognitiva',
                'slug': 'reabilitacao-neurocognitiva',
                'area': areas_map.get('neuropsicologia'),
                'titulo': 'Reabilitação Neurocognitiva',
                'subtitulo': 'Desenvolvimento e adaptação de recursos cognitivos',
                'resumo': 'Estratégias individualizadas voltadas ao funcionamento cognitivo no cotidiano.',
                'descricao': (
                    'Após avaliação prévia e indicação técnica, aplicam-se treinos e adaptações '
                    'para estimular ou compensar funções cognitivas na vida diária.'
                ),
                'icone': 'flor',
                'ordem': 5,
            },
            {
                'nome': 'Acompanhamento em Traumas',
                'slug': 'acompanhamento-traumas',
                'area': areas_map.get('traumas'),
                'titulo': 'Traumas e Experiências Difíceis',
                'subtitulo': 'Cuidado respeitoso com marcas do passado',
                'resumo': 'Quando uma experiência termina, suas marcas podem permanecer.',
                'descricao': (
                    'Experiências difíceis podem repercutir em emoções, pensamentos e relações. '
                    'O acompanhamento auxilia na elaboração dessas repercussões, respeitando seu ritmo.'
                ),
                'frase_destaque': 'Uma experiência difícil não precisa definir toda a sua história.',
                'icone': 'flor',
                'ordem': 6,
            },
            {
                'nome': 'Separação e Recomeços',
                'slug': 'atendimento-separacao',
                'area': areas_map.get('separacao-e-recomecos'),
                'titulo': 'Separação e Recomeços',
                'subtitulo': 'Reorganizando a própria vida emocional',
                'resumo': 'Separar-se também é reorganizar a própria vida e reencontrar a própria identidade.',
                'descricao': (
                    'O término de uma relação exige acolhimento de sentimentos contraditórios '
                    'e reconstrução do projeto de vida pessoal e afetivo.'
                ),
                'frase_destaque': 'Antes de escolher novamente alguém, talvez seja importante reencontrar você.',
                'icone': 'perfil',
                'ordem': 7,
            },
            {
                'nome': 'Novos Relacionamentos',
                'slug': 'novos-relacionamentos-atendimento',
                'area': areas_map.get('novos-relacionamentos'),
                'titulo': 'Novos Relacionamentos',
                'subtitulo': 'Compreendendo histórias passadas para viver o presente',
                'resumo': 'Recomeçar não significa esquecer. Fortalecimento de limites e escolhas afetivas.',
                'descricao': (
                    'A terapia auxilia a identificar padrões relacionais anteriores, superando medos '
                    'e estabelecendo limites saudáveis em novas etapas da vida amorosa.'
                ),
                'frase_destaque': 'Recomeçar não significa esquecer.',
                'icone': 'cerebro',
                'ordem': 8,
            },
        ]

        for s_dados in servicos_dados:
            slug = s_dados['slug']
            servico, criada = Servico.objects.get_or_create(
                slug=slug,
                defaults=s_dados
            )
            status = 'Criado' if criada else 'Já existente'
            self.stdout.write(f'  [Servico] {status}: {servico.nome}')

        # 5. Categorias Editoriais do Blog
        categorias_artigos_dados = [
            {
                'nome': 'Psicologia Clínica',
                'slug': 'psicologia-clinica',
                'descricao': 'Artigos e orientações sobre psicoterapia, saúde mental e autoconhecimento.',
                'ordem': 1,
            },
            {
                'nome': 'Relacionamentos',
                'slug': 'relacionamentos',
                'descricao': 'Conteúdos sobre dinâmicas afetivas, limites emocionais e recomeços saudáveis.',
                'ordem': 2,
            },
            {
                'nome': 'Traumas e Recomeços',
                'slug': 'traumas-e-recomecos',
                'descricao': 'Textos educativos sobre elaboração de experiências difíceis e reconstrução de vida.',
                'ordem': 3,
            },
            {
                'nome': 'Neuropsicologia e Avaliação',
                'slug': 'neuropsicologia-e-avaliacao',
                'descricao': 'Orientações técnicas sobre cognição, avaliação neuropsicológica e reabilitação cognitiva.',
                'ordem': 4,
            },
        ]

        cat_map = {}
        for c_dados in categorias_artigos_dados:
            c_slug = c_dados['slug']
            cat, criada = CategoriaArtigo.objects.get_or_create(
                slug=c_slug,
                defaults=c_dados
            )
            cat_map[c_slug] = cat
            status = 'Criada' if criada else 'Já existente'
            self.stdout.write(f'  [CategoriaArtigo] {status}: {cat.nome}')

        # 6. Tópicos Oficiais Fornecidos pelo Cliente (Cadastrados estritamente como RASCUNHO)
        servicos_bd = {s.slug: s for s in Servico.objects.all()}
        topicos_rascunhos = [
            {
                'titulo': 'O que acontece na primeira sessão de psicoterapia?',
                'slug': 'o-que-acontece-na-primeira-sessao-de-psicoterapia',
                'categoria_slug': 'psicologia-clinica',
                'servico_slug': 'psicologia-clinica',
            },
            {
                'titulo': 'Como saber se preciso de psicoterapia ou avaliação neuropsicológica?',
                'slug': 'como-saber-se-preciso-de-psicoterapia-ou-avaliacao-neuropsicologica',
                'categoria_slug': 'neuropsicologia-e-avaliacao',
                'servico_slug': 'avaliacao-neuropsicologica',
            },
            {
                'titulo': 'Avaliação Neuropsicológica em adultos: quando é indicada?',
                'slug': 'avaliacao-neuropsicologica-em-adultos-quando-e-indicada',
                'categoria_slug': 'neuropsicologia-e-avaliacao',
                'servico_slug': 'avaliacao-neuropsicologica',
            },
            {
                'titulo': 'Memória fraca ou sobrecarga emocional? Como diferenciar',
                'slug': 'memoria-fraca-ou-sobrecarga-emocional-como-diferenciar',
                'categoria_slug': 'neuropsicologia-e-avaliacao',
                'servico_slug': 'avaliacao-neuropsicologica',
            },
            {
                'titulo': 'Separação conjugal: quando o término exige reconstrução emocional',
                'slug': 'separacao-conjugal-quando-o-termino-exige-reconstrucao-emocional',
                'categoria_slug': 'relacionamentos',
                'servico_slug': 'atendimento-separacao',
            },
            {
                'titulo': 'Por que repetimos padrões nos relacionamentos?',
                'slug': 'por-que-repetimos-padroes-nos-relacionamentos',
                'categoria_slug': 'relacionamentos',
                'servico_slug': 'novos-relacionamentos-atendimento',
            },
            {
                'titulo': 'Traumas não elaborados: sinais de que o passado ainda impacta o presente',
                'slug': 'traumas-nao-elaborados-sinais-de-que-o-passado-ainda-impacta-o-presente',
                'categoria_slug': 'traumas-e-recomecos',
                'servico_slug': 'acompanhamento-traumas',
            },
            {
                'titulo': 'Quando a reabilitação neurocognitiva pode ajudar na rotina',
                'slug': 'quando-a-reabilitacao-neurocognitiva-pode-ajudar-na-rotina',
                'categoria_slug': 'neuropsicologia-e-avaliacao',
                'servico_slug': 'reabilitacao-neurocognitiva',
            },
            {
                'titulo': 'Cuidar de si não é egoísmo: limites saudáveis na vida emocional',
                'slug': 'cuidar-de-si-nao-e-egoismo-limites-saudaveis-na-vida-emocional',
                'categoria_slug': 'psicologia-clinica',
                'servico_slug': 'psicologia-clinica',
            },
        ]

        for t_dados in topicos_rascunhos:
            t_slug = t_dados['slug']
            cat_obj = cat_map.get(t_dados['categoria_slug'])
            serv_obj = servicos_bd.get(t_dados['servico_slug'])
            artigo, criada = Artigo.objects.get_or_create(
                slug=t_slug,
                defaults={
                    'titulo': t_dados['titulo'],
                    'categoria': cat_obj,
                    'autor': prof,
                    'servico_relacionado': serv_obj,
                    'status': Artigo.STATUS_RASCUNHO,
                    'conteudo': '',
                    'resumo': '',
                    'destaque': False,
                    'data_publicacao': None,
                }
            )
            status = 'Criado (Rascunho)' if criada else 'Já existente'
            self.stdout.write(f'  [Artigo] {status}: {artigo.titulo}')

        self.stdout.write(self.style.SUCCESS('Carga de dados institucionais concluída com sucesso!'))

