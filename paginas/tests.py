"""
Testes automatizados do app paginas.
Cobre a Home definitiva (Prompt 05), o laboratório do Design System e os componentes globais.
"""
from django.test import TestCase
from django.urls import reverse
from nucleo.models import ConfiguracaoSite, Profissional, RedeSocial
from servicos.models import AreaAtuacao, Servico


class HomeViewTests(TestCase):
    """Testes completos da página inicial (Home) do Instituto Mente em Foco."""

    def setUp(self):
        """Prepara dados institucionais para a Home."""
        self.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            slogan_principal="COMPREENDER • CUIDAR • RECONSTRUIR",
            frase_institucional="Psicologia e Neuropsicologia integrada.",
            whatsapp="5561999998888",
            mensagem_whatsapp_padrao="Olá, gostaria de informações sobre atendimento.",
            ativo=True
        )

        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Psicóloga Mari Menezes",
            slug="mari-menezes",
            titulo_profissional="Psicóloga, palestrante e facilitadora de grupos",
            atuacao_resumida="Psicologia e Neuropsicologia",
            biografia_curta="Minha prática parte da compreensão de que cada pessoa carrega uma história.",
            frase_destaque="Meu propósito é ajudar pessoas a compreenderem melhor a própria história.",
            ativo=True
        )

        self.area1 = AreaAtuacao.objects.create(
            nome="Psicologia",
            slug="psicologia",
            titulo="Psicologia Clínica",
            resumo="Compreenda suas emoções e relações.",
            ordem=1,
            ativo=True,
            mostrar_na_home=True
        )

        self.area2 = AreaAtuacao.objects.create(
            nome="Neuropsicologia",
            slug="neuropsicologia",
            titulo="Neuropsicologia Clínica",
            resumo="Entenda a relação entre cérebro e cognição.",
            ordem=2,
            ativo=True,
            mostrar_na_home=True
        )

        self.area_inativa = AreaAtuacao.objects.create(
            nome="Área Não Ativa",
            slug="area-inativa",
            titulo="Inativa",
            resumo="Não deve aparecer na Home.",
            ordem=99,
            ativo=False,
            mostrar_na_home=True
        )

    def test_rota_raiz_retorna_200(self):
        """A rota raiz / deve responder com status HTTP 200."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(response.status_code, 200)

    def test_templates_utilizados(self):
        """A view deve renderizar home.html herdando de base.html."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertTemplateUsed(response, 'paginas/home.html')
        self.assertTemplateUsed(response, 'base/base.html')

    def test_h1_unico_e_exato(self):
        """O H1 deve ser único na página e conter exatamente a frase mestra aprovada."""
        response = self.client.get(reverse('paginas:inicio'))
        conteudo = response.content.decode('utf-8')
        # Verifica ocorrência única da tag h1
        self.assertEqual(conteudo.count('<h1'), 1, "A Home deve conter rigorosamente uma tag <h1>.")
        self.assertContains(response, 'Psicologia Clínica e <em>Avaliação neuropsicológica</em>')

    def test_eyebrow_oficial_presente(self):
        """O conceito tríplice oficial deve estar no eyebrow do Hero."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'COMPREENDER • CUIDAR • RECONSTRUIR')

    def test_profissional_exibida_quando_ativa(self):
        """A profissional Mari Menezes deve ter seus dados exibidos quando ativa."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'Psicóloga Mari Menezes')
        self.assertContains(response, 'Prazer, eu sou <em>Mari Menezes.</em>')
        self.assertContains(response, 'Minha prática parte da compreensão')
        self.assertContains(response, 'escuta, investigação e cuidado')

    def test_profissional_inativa_nao_quebra_pagina(self):
        """Se a profissional estiver inativa, a Home não deve quebrar e mantém fallbacks seguros."""
        self.profissional.ativo = False
        self.profissional.save()

        response = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prazer, eu sou <em>Mari Menezes.</em>')

    def test_areas_atuacao_ordem_e_filtro(self):
        """Somente áreas ativas e marcadas para a Home devem ser listadas, na ordem correta."""
        response = self.client.get(reverse('paginas:inicio'))
        conteudo = response.content.decode('utf-8')

        # Áreas ativas presentes
        self.assertContains(response, 'Psicologia')
        self.assertContains(response, 'Neuropsicologia')
        # Área inativa ausente
        self.assertNotContains(response, 'Área Não Ativa')

        # Ordem: Psicologia antes de Neuropsicologia
        pos_psico = conteudo.find('Psicologia')
        pos_neuro = conteudo.find('Neuropsicologia')
        self.assertTrue(pos_psico < pos_neuro, "As áreas de atuação devem respeitar o campo ordem.")

    def test_cards_identificacao_sem_diagnostico(self):
        response = self.client.get(reverse('paginas:inicio'))
        for slug in ['burnout', 'cirurgia-bariatrica', 'esterilizacao', 'inss', 'processos-judiciais', 'ansiedade-depressao']:
            self.assertContains(response, '/servicos/avaliacao/' + slug + '/')
        self.assertNotContains(response, 'Você tem depressão')
        self.assertNotContains(response, 'aprovação garantida')

    def test_etapas_atendimento_01_a_04(self):
        response = self.client.get(reverse('paginas:inicio'))
        for etapa in ['Entender a demanda', 'Planejar a avaliação', 'Investigar com cuidado', 'Devolver e orientar']:
            self.assertContains(response, etapa)

    def test_bloco_neuropsicologia_e_avaliacao(self):
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'Avaliações Psicológicas, Laudos e Pareceres')
        self.assertContains(response, 'Responsabilidade Técnica e Ética')
        html = response.content.decode('utf-8')
        self.assertLess(html.index('id="avaliacoes"'), html.index('id="atendimento"'))
        self.assertContains(response, '/servicos/neuropsicologia/')

    def test_faq_itens_presentes(self):
        """A seção de FAQ deve renderizar perguntas frequentes com details e summary."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'Como solicitar uma avaliação psicológica?')
        self.assertContains(response, 'Toda avaliação resulta em laudo?')
        self.assertContains(response, 'O atendimento pode ser online?')
        self.assertContains(response, '<details', html=False)
        self.assertContains(response, '<summary', html=False)

    def test_cta_final_presente(self):
        """A seção final de CTA deve conter a frase e botão oficiais."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'Cuidar da mente também é uma forma de recomeçar.')
        self.assertContains(response, 'Agendar atendimento')

    def test_home_assets_carregados(self):
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'css/editorial.css')
        self.assertContains(response, 'js/navegacao.js')
        self.assertContains(response, 'img/avaliacoes/burnout-v2.webp')

    def test_ausencia_dados_ficticios(self):
        """A Home não deve conter depoimentos fictícios, números inventados ou CRP falso."""
        response = self.client.get(reverse('paginas:inicio'))
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('+500 pacientes', conteudo)
        self.assertNotIn('10 anos de experiência', conteudo)
        self.assertNotIn('98% de satisfação', conteudo)
        self.assertNotIn('Depoimentos', conteudo)
        self.assertNotIn('PENDENTE_DEFINICAO', conteudo)


class DesignSystemLaboratorioTests(TestCase):
    """Testes para a página interna /design-system/."""

    def test_laboratorio_retorna_200_em_debug(self):
        """Com DEBUG=True, a página /design-system/ deve responder com status 200."""
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('paginas:laboratorio_design_system'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'paginas/laboratorio_design_system.html')
            self.assertContains(response, 'LABORATÓRIO VISUAL')
            self.assertContains(response, 'Bege Areia')
            self.assertContains(response, 'Verde Oliva')
            self.assertContains(response, 'titulo-hero')
            self.assertContains(response, 'fileira-identificacao')
            self.assertContains(response, 'placeholder-imagem')

    def test_laboratorio_retorna_404_em_producao(self):
        """Com DEBUG=False, a página /design-system/ deve retornar status 404 (bloqueio seguro)."""
        with self.settings(DEBUG=False):
            response = self.client.get(reverse('paginas:laboratorio_design_system'))
            self.assertEqual(response.status_code, 404)


class GlobalInterfaceStructureTests(TestCase):
    """Testes automatizados da infraestrutura global (Header, Footer, Menu, WhatsApp, CMS)."""

    def setUp(self):
        """Cria configuração inicial para os testes."""
        self.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            slogan_principal="COMPREENDER • CUIDAR • RECONSTRUIR",
            frase_institucional="Psicologia e Neuropsicologia integrada.",
            whatsapp="",  # Inicialmente vazio para testar fallbacks
            email="",
            instagram="",
            ativo=True
        )

    def test_header_e_footer_presentes_na_pagina_inicial(self):
        """A página inicial deve renderizar o Header definitivo e o Footer institucional."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<header class="site-header"', html=False)
        self.assertContains(response, '<footer class="site-footer"', html=False)
        self.assertContains(response, 'skip-link')

    def test_menu_navegacao_contem_itens_oficiais(self):
        """O menu deve apresentar todos os links oficiais planejados com URLs nomeadas válidas."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, reverse('paginas:inicio'))
        self.assertContains(response, reverse('paginas:sobre_mim'))
        self.assertContains(response, reverse('servicos:psicologia'))
        self.assertContains(response, reverse('servicos:neuropsicologia'))
        self.assertContains(response, reverse('servicos:traumas'))
        self.assertContains(response, reverse('servicos:separacao_recomecos'))
        self.assertContains(response, reverse('servicos:avaliacao'))
        self.assertContains(response, reverse('conteudos:index'))
        self.assertContains(response, reverse('contato:index'))

    def test_estado_ativo_na_pagina_inicial(self):
        """Na rota raiz /, o link de Início deve receber o atributo aria-current="page"."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'site-nav__link--ativo')

    def test_botao_mobile_atributos_acessibilidade(self):
        """O botão do menu mobile deve possuir os atributos de acessibilidade adequados."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'data-menu-toggle')
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'aria-controls="menu-mobile-painel"')
        self.assertContains(response, 'data-menu-panel')

    def test_fallback_logo_quando_sem_imagem(self):
        """Sem imagem de logo cadastrada, deve exibir o fallback tipográfico sem erros."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'site-logo__nome')
        self.assertContains(response, 'Instituto Mente em Foco')

    def test_whatsapp_ausente_nao_gera_botao_flutuante_nem_link_quebrado(self):
        """Sem número de WhatsApp cadastrado, o botão flutuante não deve aparecer e o CTA aponta para contato."""
        self.config.whatsapp = ""
        self.config.save()

        response = self.client.get(reverse('paginas:inicio'))
        # Botão flutuante não deve existir
        self.assertNotContains(response, 'class="whatsapp-flutuante"')
        # Não deve conter wa.me quebrado
        self.assertNotContains(response, 'https://wa.me/?')
        self.assertNotContains(response, 'https://wa.me/')
        # CTA deve apontar com segurança para a página de contato
        self.assertContains(response, reverse('contato:index'))

    def test_whatsapp_configurado_gera_botao_flutuante_e_link_valido(self):
        """Com número de WhatsApp cadastrado, gera o botão flutuante e link wa.me devidamente codificado."""
        self.config.whatsapp = "5561999998888"
        self.config.mensagem_whatsapp_padrao = "Olá, gostaria de agendar uma consulta."
        self.config.save()

        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'class="whatsapp-flutuante"')
        self.assertContains(response, 'https://wa.me/5561999998888?text=')
        # Mensagem deve estar URL encoded
        self.assertContains(response, 'Ol%C3%A1')

    def test_redes_sociais_condicionais(self):
        """Redes ativas com URL válida aparecem no rodapé; redes vazias ou inativas não aparecem."""
        RedeSocial.objects.create(
            nome="Instagram Oficial",
            url="https://instagram.com/institutomentemfoco",
            icone="instagram",
            ativo=True,
            ordem=1
        )
        RedeSocial.objects.create(
            nome="Rede Inativa",
            url="https://exemplo.com/inativo",
            icone="outro",
            ativo=False,
            ordem=2
        )
        RedeSocial.objects.create(
            nome="Rede Pendente",
            url="PENDENTE_DEFINICAO",
            icone="facebook",
            ativo=True,
            ordem=3
        )

        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'https://instagram.com/institutomentemfoco')
        self.assertNotContains(response, 'https://exemplo.com/inativo')
        self.assertNotContains(response, 'PENDENTE_DEFINICAO')

    def test_sem_lixo_visual_quando_campos_opcionais_vazios(self):
        """A interface nunca deve renderizar strings de desenvolvimento como None, null ou PENDENTE_DEFINICAO."""
        response = self.client.get(reverse('paginas:inicio'))
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('PENDENTE_DEFINICAO', conteudo)
        self.assertNotIn('None', conteudo)
        self.assertNotIn('null', conteudo)

    def test_script_navegacao_carregado_com_defer(self):
        """O script navegacao.js deve ser carregado com o atributo defer."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertContains(response, 'js/navegacao.js')
        self.assertContains(response, '<script src="/static/js/navegacao.js" defer></script>')


class SobreMimPaginaTests(TestCase):
    """Testes para a página interna /sobre-mim/."""

    def setUp(self):
        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Psicóloga Mari Menezes",
            slug="mari-menezes",
            titulo_profissional="Psicóloga, palestrante e facilitadora de grupos",
            atuacao_resumida="Psicologia e Neuropsicologia",
            biografia_curta="Minha prática parte da compreensão de que cada pessoa carrega uma história que precisa ser compreendida antes de ser julgada.",
            frase_destaque="Meu propósito é ajudar pessoas a compreenderem melhor a própria história e encontrarem recursos para seguir seus caminhos.",
            registro_profissional="CRP 03/10838",
            ativo=True
        )

    def test_sobre_mim_status_200_e_template(self):
        """A rota /sobre-mim/ deve responder HTTP 200 e utilizar o template correto."""
        response = self.client.get(reverse('paginas:sobre_mim'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/sobre_mim.html')
        self.assertTemplateUsed(response, 'base/base.html')

    def test_sobre_mim_h1_oficial(self):
        """O H1 deve ser exatamente 'Prazer, eu sou Mari Menezes.'."""
        response = self.client.get(reverse('paginas:sobre_mim'))
        self.assertContains(response, 'Prazer, eu sou Mari Menezes.')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Prazer, eu sou Mari Menezes.</h1>')

    def test_sobre_mim_conteudo_oficial(self):
        """Apresentação, biografia oficial e frase de destaque devem estar presentes."""
        response = self.client.get(reverse('paginas:sobre_mim'))
        self.assertContains(response, 'Psicóloga Clínica e Avaliadora Psicológica')
        self.assertContains(response, 'Minha prática parte da compreensão')
        self.assertContains(response, 'Meu propósito é ajudar pessoas a compreenderem melhor a própria história')
        self.assertContains(response, 'CRP 03/10838')

    def test_sobre_mim_pilares_clinicos(self):
        """Os 3 pilares clínicos (Compreender, Cuidar, Reconstruir) devem estar presentes."""
        response = self.client.get(reverse('paginas:sobre_mim'))
        self.assertContains(response, 'Compreender')
        self.assertContains(response, 'Cuidar')
        self.assertContains(response, 'Reconstruir')

    def test_sobre_mim_assets_e_ausencia_dados_ficticios(self):
        """CSS de páginas internas deve ser carregado e não deve haver lixo visual."""
        response = self.client.get(reverse('paginas:sobre_mim'))
        self.assertContains(response, 'css/paginas_internas.css')
        conteudo = response.content.decode('utf-8')
        self.assertNotIn('PENDENTE_DEFINICAO', conteudo)
        self.assertNotIn('Universidade Federal', conteudo)
        self.assertNotIn('+500 pacientes', conteudo)


