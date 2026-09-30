from django.test import TestCase
from django.contrib.auth.models import User
from servicos.models import AreaAtuacao, Servico


class ServicosModelsTests(TestCase):
    """Testes dos models de Áreas de Atuação e Serviços."""

    def test_area_atuacao_criacao_e_slug(self):
        """AreaAtuacao deve gerar slug seguro a partir do nome."""
        area = AreaAtuacao.objects.create(
            nome="Neuropsicologia",
            titulo="Neuropsicologia Clínica",
            resumo="Compreensão da relação entre cérebro e cognição."
        )
        self.assertEqual(area.slug, "neuropsicologia")
        self.assertEqual(str(area), "Neuropsicologia")
        self.assertTrue(area.ativo)
        self.assertTrue(area.mostrar_na_home)

    def test_servico_criacao_e_relacionamento(self):
        """Servico deve associar-se à AreaAtuacao e gerar slug único."""
        area = AreaAtuacao.objects.create(
            nome="Psicologia",
            titulo="Psicologia Clínica",
            resumo="Acompanhamento psicológico."
        )
        servico = Servico.objects.create(
            nome="Psicoterapia Individual",
            titulo="Psicoterapia Individual",
            resumo="Espaço de escuta profissional.",
            descricao="Atendimento clínico humanizado.",
            area=area,
            ordem=1
        )
        self.assertEqual(servico.slug, "psicoterapia-individual")
        self.assertEqual(str(servico), "Psicoterapia Individual")
        self.assertEqual(servico.area, area)
        self.assertIn(servico, area.servicos.all())

    def test_ordenacao_servicos(self):
        """Servicos devem respeitar o campo 'ordem'."""
        s2 = Servico.objects.create(nome="Serviço B", titulo="B", resumo="...", descricao="...", ordem=2)
        s1 = Servico.objects.create(nome="Serviço A", titulo="A", resumo="...", descricao="...", ordem=1)
        
        lista = list(Servico.objects.all())
        self.assertEqual(lista[0], s1)
        self.assertEqual(lista[1], s2)


class ServicosAdminTests(TestCase):
    """Testes de acesso ao admin para servicos."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin_servicos', 'admin@teste.com', 'SenhaForte123!')
        self.client.force_login(self.admin_user)

    def test_admin_area_atuacao_acessivel(self):
        """Painel de AreaAtuacao deve responder HTTP 200."""
        response = self.client.get('/admin/servicos/areaatuacao/')
        self.assertEqual(response.status_code, 200)

    def test_admin_servico_acessivel(self):
        """Painel de Servico deve responder HTTP 200."""
        response = self.client.get('/admin/servicos/servico/')
        self.assertEqual(response.status_code, 200)


class PaginasEixoPsicologiaTests(TestCase):
    """Testes completos das 4 páginas de serviços do Eixo Psicologia."""

    def setUp(self):
        self.area_psico = AreaAtuacao.objects.create(
            nome="Psicologia",
            slug="psicologia",
            titulo="Psicologia Clínica",
            resumo="Compreenda suas emoções e relações."
        )
        self.servico_psico = Servico.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            titulo="Psicologia e Psicoterapia",
            resumo="Um espaço de escuta profissional para compreender emoções, pensamentos, comportamentos e relações.",
            descricao="A psicoterapia oferece um espaço ético e sigiloso para acolher suas experiências emocionais.",
            area=self.area_psico,
            ordem=1,
            ativo=True
        )

        self.area_traumas = AreaAtuacao.objects.create(
            nome="Traumas",
            slug="traumas",
            titulo="Traumas e Experiências Difíceis",
            resumo="Elabore vivências difíceis com cuidado."
        )
        self.servico_traumas = Servico.objects.create(
            nome="Acompanhamento em Traumas",
            slug="acompanhamento-traumas",
            titulo="Traumas e Experiências Difíceis",
            resumo="Quando uma experiência termina, suas marcas podem permanecer.",
            descricao="Experiências difíceis podem repercutir em emoções, pensamentos e relações.",
            frase_destaque="Uma experiência difícil não precisa definir toda a sua história.",
            area=self.area_traumas,
            ordem=2,
            ativo=True
        )

        self.area_separacao = AreaAtuacao.objects.create(
            nome="Separação e Recomeços",
            slug="separacao-e-recomecos",
            titulo="Separação e Recomeços",
            resumo="Reorganize sua vida emocional."
        )
        self.servico_separacao = Servico.objects.create(
            nome="Separação e Recomeços",
            slug="atendimento-separacao",
            titulo="Separação e Recomeços",
            resumo="Separar-se também é reorganizar a própria vida.",
            descricao="O término de uma relação exige acolhimento de sentimentos contraditórios.",
            frase_destaque="Antes de escolher novamente alguém, talvez seja importante reencontrar você.",
            area=self.area_separacao,
            ordem=3,
            ativo=True
        )

        self.area_relacionamentos = AreaAtuacao.objects.create(
            nome="Novos Relacionamentos",
            slug="novos-relacionamentos",
            titulo="Novos Relacionamentos",
            resumo="Compreenda seu passado e fortaleça seus limites."
        )
        self.servico_relacionamentos = Servico.objects.create(
            nome="Novos Relacionamentos",
            slug="novos-relacionamentos-atendimento",
            titulo="Novos Relacionamentos",
            resumo="Recomeçar não significa esquecer.",
            descricao="A terapia auxilia a identificar padrões relacionais anteriores, superando medos.",
            frase_destaque="Recomeçar não significa esquecer.",
            area=self.area_relacionamentos,
            ordem=4,
            ativo=True
        )

    # --- PSICOLOGIA ---
    def test_psicologia_status_200_e_template(self):
        """A página de Psicologia deve responder HTTP 200 e carregar template e CSS corretos."""
        response = self.client.get('/servicos/psicologia/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/psicologia.html')
        self.assertContains(response, 'css/editorial.css')

    def test_psicologia_h1_e_frase_base(self):
        """Deve conter o H1 e mensagem base oficiais de Psicologia."""
        response = self.client.get('/servicos/psicologia/')
        self.assertContains(response, '<h1>Psicoterapia Humanizada para Promoção da Saúde Mental e Qualidade de Vida</h1>')
        self.assertContains(response, 'Você não precisa ter todas as respostas para começar.')

    def test_psicologia_temas_clinicos_e_sem_promessas(self):
        """Os temas clínicos essenciais devem estar presentes sem promessas milagrosas."""
        response = self.client.get('/servicos/psicologia/')
        self.assertContains(response, 'Ansiedade')
        self.assertContains(response, 'autoestima')
        self.assertContains(response, 'Relacionamentos')
        self.assertContains(response, 'Separação e recomeços')
        self.assertContains(response, 'perdas, mudanças')
        self.assertContains(response, 'desenvolvimento pessoal')
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('Curamos ansiedade', conteudo)
        self.assertNotIn('Eliminamos traumas', conteudo)

    # --- TRAUMAS ---
    def test_traumas_status_200_e_template(self):
        """A página de Traumas deve responder HTTP 200 e carregar template correto."""
        response = self.client.get('/servicos/traumas/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/traumas.html')

    def test_traumas_h1_e_frases_oficiais(self):
        """Deve conter a mensagem principal e a frase de destaque oficial."""
        response = self.client.get('/servicos/traumas/')
        self.assertContains(response, 'Traumas e Experiências Difíceis')
        self.assertContains(response, 'Quando uma experiência termina, suas marcas podem permanecer.')
        self.assertContains(response, 'Uma experiência difícil não precisa definir toda a sua história.')

    def test_traumas_repercussoes_e_sem_sensacionalismo(self):
        """Deve apresentar os 4 eixos de repercussão sem prometer 'apagar o passado'."""
        response = self.client.get('/servicos/traumas/')
        self.assertContains(response, 'Emoções')
        self.assertContains(response, 'Pensamentos')
        self.assertContains(response, 'Comportamentos')
        self.assertContains(response, 'Relações')
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('Apague as marcas', conteudo)
        self.assertNotIn('Cure-se do trauma', conteudo)
        self.assertNotIn('Nunca mais sofra', conteudo)

    # --- SEPARAÇÃO & RECOMEÇOS ---
    def test_separacao_status_200_e_template(self):
        """A página de Separação & Recomeços deve responder HTTP 200."""
        response = self.client.get('/servicos/separacao-e-recomecos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/separacao_recomecos.html')

    def test_separacao_h1_e_frases_oficiais(self):
        """Deve conter o H1, frase principal e frase de destaque."""
        response = self.client.get('/servicos/separacao-e-recomecos/')
        self.assertContains(response, 'Separação e Recomeços')
        self.assertContains(response, 'Separar-se também é reorganizar a própria vida.')
        self.assertContains(response, 'Antes de escolher novamente alguém, talvez seja importante reencontrar você.')
        self.assertContains(response, 'Recomeçar não significa esquecer')

    def test_separacao_aspectos_trabalhados(self):
        """Deve apresentar aspectos da reorganização (rotina, sentimentos contraditórios, identidade)."""
        response = self.client.get('/servicos/separacao-e-recomecos/')
        self.assertContains(response, 'A Rotina')
        self.assertContains(response, 'Sentimentos Contraditórios')
        self.assertContains(response, 'Autoestima')
        self.assertContains(response, 'Reconstrução da Identidade')
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('parceiro narcisista', conteudo)
        self.assertNotIn('5 fases do luto', conteudo)

    # --- NOVOS RELACIONAMENTOS ---
    def test_novos_relacionamentos_status_200_e_template(self):
        """A página de Novos Relacionamentos deve responder HTTP 200."""
        response = self.client.get('/servicos/novos-relacionamentos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/novos_relacionamentos.html')

    def test_novos_relacionamentos_h1_e_dois_eixos(self):
        """Deve conter H1, frase mestre e os dois eixos reflexivos (desejo e cautela)."""
        response = self.client.get('/servicos/novos-relacionamentos/')
        self.assertContains(response, 'Novos Relacionamentos')
        self.assertContains(response, 'Recomeçar não significa esquecer')
        self.assertContains(response, 'Vontade de se envolver novamente')
        self.assertContains(response, 'O medo de sofrer novamente')
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('Quiz de amor', conteudo)
        self.assertNotIn('Descubra se você está pronto para amar', conteudo)


class EixoTecnicoTests(TestCase):
    """Testes completos das 5 páginas e componentes do Eixo Técnico (Prompt 08)."""

    def setUp(self):
        self.area_neuro = AreaAtuacao.objects.create(
            nome="Neuropsicologia",
            slug="neuropsicologia",
            titulo="Neuropsicologia Clínica",
            resumo="Investigação das relações entre funcionamento cerebral, cognição e comportamento.",
            ordem=2,
            ativo=True
        )
        self.servico_neuro = Servico.objects.create(
            nome="Neuropsicologia Clínica",
            slug="neuropsicologia-clinica",
            titulo="Neuropsicologia",
            resumo="Uma área da Psicologia que investiga as relações entre funcionamento cerebral, cognição, emoções e comportamento.",
            descricao="Por meio de uma escuta técnica, fundamentada e acolhedora, a prática neuropsicológica busca identificar potencialidades.",
            area=self.area_neuro,
            ordem=2,
            ativo=True
        )

        self.area_psico = AreaAtuacao.objects.create(
            nome="Psicologia",
            slug="psicologia",
            titulo="Psicologia Clínica",
            resumo="Espaço de escuta profissional.",
            ordem=1,
            ativo=True
        )
        self.servico_aval_psico = Servico.objects.create(
            nome="Avaliação Psicológica",
            slug="avaliacao-psicologica",
            titulo="Avaliação Psicológica",
            resumo="Processo estruturado de compreensão técnica de aspectos emocionais, comportamentais e relacionais.",
            descricao="O processo é organizado de acordo com os objetivos e a demanda específica de cada pessoa.",
            area=self.area_psico,
            ordem=3,
            ativo=True
        )

        self.servico_aval_neuro = Servico.objects.create(
            nome="Avaliação Neuropsicológica",
            slug="avaliacao-neuropsicologica",
            titulo="Avaliação Neuropsicológica",
            resumo="Mapeamento minucioso do perfil cognitivo e funcional por meio de procedimentos técnicos e instrumentos padronizados.",
            descricao="O processo possibilita traçar um panorama detalhado de forças cognitivas e áreas que demandam atenção.",
            area=self.area_neuro,
            ordem=4,
            ativo=True
        )

        self.servico_reab = Servico.objects.create(
            nome="Reabilitação Neurocognitiva",
            slug="reabilitacao-neurocognitiva",
            titulo="Reabilitação Neurocognitiva",
            resumo="Após avaliação e quando houver indicação, construção de estratégias individualizadas voltadas ao funcionamento cognitivo.",
            descricao="O trabalho visa ao fortalecimento da autonomia no cotidiano por meio da construção e aplicação de estratégias individualizadas.",
            area=self.area_neuro,
            ordem=5,
            ativo=True
        )

    # --- 1. NEUROPSICOLOGIA ---
    def test_neuropsicologia_status_200_e_template(self):
        """A página de Neuropsicologia deve responder 200 e carregar template e CSS corretos."""
        response = self.client.get('/servicos/neuropsicologia/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/neuropsicologia.html')
        self.assertContains(response, 'css/paginas_internas.css')

    def test_neuropsicologia_h1_e_aspectos_cognitivos(self):
        """Deve conter H1 oficial, 8 aspectos cognitivos e ressalva 'conforme a demanda'."""
        response = self.client.get('/servicos/neuropsicologia/')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Neuropsicologia</h1>')
        self.assertContains(response, 'funcionamento cerebral')
        self.assertContains(response, 'cognição')
        self.assertContains(response, 'emoções')
        self.assertContains(response, 'comportamento')
        self.assertContains(response, 'Atenção')
        self.assertContains(response, 'Memória')
        self.assertContains(response, 'Funções Executivas')
        self.assertContains(response, 'Raciocínio')
        self.assertContains(response, 'Linguagem')
        self.assertContains(response, 'Aspectos Emocionais')
        self.assertContains(response, 'Funcionamento Cognitivo')
        self.assertContains(response, 'conforme a demanda')

        # Vedações éticas
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('Procure se esquecer nomes', conteudo)
        self.assertNotIn('diagnóstico definitivo', conteudo)

    # --- 2. HUB DE AVALIAÇÃO ---
    def test_avaliacao_hub_status_200_e_diferenciacao(self):
        """A página Hub de Avaliação deve responder 200 e diferenciar os dois processos."""
        response = self.client.get('/servicos/avaliacao/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/avaliacao_hub.html')
        self.assertContains(response, 'Avaliações Psicológicas,<br><em>Laudos e Pareceres</em>')
        self.assertContains(response, 'Cada documento tem')
        self.assertContains(response, '/servicos/avaliacao-psicologica/')
        self.assertContains(response, '/servicos/avaliacao-neuropsicologica/')

    # --- 3. AVALIAÇÃO PSICOLÓGICA ---
    def test_avaliacao_psicologica_status_200_e_fluxo(self):
        """Deve responder 200, conter H1 exato e o fluxo oficial de 6 etapas."""
        response = self.client.get('/servicos/avaliacao-psicologica/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/avaliacao_psicologica.html')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Avaliação Psicológica</h1>')

        # Breadcrumb hierárquico
        self.assertContains(response, 'href="/servicos/avaliacao/"')

        # 6 Etapas do fluxo oficial
        self.assertContains(response, 'Entrevista')
        self.assertContains(response, 'Aplicação de instrumentos')
        self.assertContains(response, 'Análise dos resultados')
        self.assertContains(response, 'Integração das informações')
        self.assertContains(response, 'Devolutiva')
        self.assertContains(response, 'Documento técnico, quando indicado')

        # Frase técnica obrigatória
        self.assertContains(response, 'A indicação e a escolha dos procedimentos devem ser definidas de acordo com a demanda e dentro dos critérios técnicos e éticos da Psicologia.')

        # Vedações de testes inventados e garantias
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('WAIS', conteudo)
        self.assertNotIn('WISC', conteudo)
        self.assertNotIn('MMPI', conteudo)
        self.assertNotIn('Rorschach', conteudo)
        self.assertNotIn('R$ ', conteudo)
        self.assertNotIn('sessões garantidas', conteudo)

    # --- 4. AVALIAÇÃO NEUROPSICOLÓGICA ---
    def test_avaliacao_neuropsicologica_status_200_e_fluxo(self):
        """Deve responder 200, conter H1 exato, aspectos e o fluxo oficial."""
        response = self.client.get('/servicos/avaliacao-neuropsicologica/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/avaliacao_neuropsicologica.html')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Avaliação Neuropsicológica</h1>')

        # 6 Etapas e orientação técnica
        self.assertContains(response, 'Entrevista')
        self.assertContains(response, 'Aplicação de instrumentos')
        self.assertContains(response, 'Análise dos resultados')
        self.assertContains(response, 'Integração das informações')
        self.assertContains(response, 'Devolutiva')
        self.assertContains(response, 'Documento técnico, quando indicado')
        self.assertContains(response, 'conforme a demanda')

        # Ponte para reabilitação
        self.assertContains(response, '/servicos/reabilitacao-neurocognitiva/')

    # --- 5. REABILITAÇÃO NEUROCOGNITIVA ---
    def test_reabilitacao_neurocognitiva_status_200_e_conceito(self):
        """Deve responder 200, conter H1 exato e mensagem oficial sem promessas."""
        response = self.client.get('/servicos/reabilitacao-neurocognitiva/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/reabilitacao_neurocognitiva.html')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Reabilitação Neurocognitiva</h1>')

        # Conceitos obrigatórios
        self.assertContains(response, 'Após avaliação e quando houver indicação')
        self.assertContains(response, 'Estratégias individualizadas')
        self.assertContains(response, 'Funcionamento Cognitivo')
        self.assertContains(response, 'Vida Cotidiana')
        self.assertContains(response, 'Necessidades e Objetivos da Pessoa')

        # Vedações de cura e promessas
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('Recupere sua memória', conteudo)
        self.assertNotIn('Volte ao normal', conteudo)
        self.assertNotIn('100% da cognição', conteudo)
        self.assertNotIn('treinamento cerebral', conteudo)

    # --- 6. ESTADO ATIVO DO MENU ---
    def test_estados_ativos_navegacao_eixo_tecnico(self):
        for path in ['/servicos/avaliacao/', '/servicos/avaliacao/burnout/', '/servicos/avaliacao/inss/']:
            response = self.client.get(path)
            self.assertContains(response, 'href="' + path + '" aria-current="page"')
        for path in ['/servicos/neuropsicologia/', '/servicos/reabilitacao-neurocognitiva/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'site-nav__dropdown')

    def test_resiliencia_servicos_ausentes_no_banco(self):
        """Se os registros de serviços forem removidos ou inativados, as páginas não devem lançar erro 500."""
        Servico.objects.all().update(ativo=False)

        rotas = [
            '/servicos/neuropsicologia/',
            '/servicos/avaliacao/',
            '/servicos/avaliacao-psicologica/',
            '/servicos/avaliacao-neuropsicologica/',
            '/servicos/reabilitacao-neurocognitiva/',
        ]

        for rota in rotas:
            with self.subTest(rota=rota):
                resp = self.client.get(rota)
                self.assertEqual(resp.status_code, 200)
