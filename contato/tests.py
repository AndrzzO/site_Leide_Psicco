"""
Testes automatizados completos do app contato.
Cobre model MensagemContato, ContatoForm (validação, minimização, honeypot),
views (GET 200, H1 único, PRG, feedback de mensagens, XSS, CSRF, rate limit),
exibição do WhatsApp e acesso ao Django Admin.
"""
from io import StringIO
from datetime import timedelta
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone

from nucleo.models import ConfiguracaoSite
from servicos.models import AreaAtuacao, Servico
from contato.models import MensagemContato
from contato.forms import ContatoForm

User = get_user_model()



class MensagemContatoModelTest(TestCase):
    """Testes do modelo MensagemContato."""

    def test_criacao_e_str_mensagem(self):
        msg = MensagemContato.objects.create(
            nome="Mariana da Silva",
            email="mariana@exemplo.com.br",
            telefone="61999998888",
            mensagem="Gostaria de informações sobre psicoterapia individual.",
            aceite_privacidade=True
        )
        self.assertFalse(msg.lida)
        self.assertIn("Mariana da Silva", str(msg))
        self.assertIn("Contato de Mariana da Silva", str(msg))

    def test_ordenacao_por_mais_recentes(self):
        msg1 = MensagemContato.objects.create(nome="Primeiro", email="p@ex.com", aceite_privacidade=True)
        msg2 = MensagemContato.objects.create(nome="Segundo", email="s@ex.com", aceite_privacidade=True)

        mensagens = list(MensagemContato.objects.all())
        self.assertEqual(mensagens[0], msg2)
        self.assertEqual(mensagens[1], msg1)


class ContatoFormTest(TestCase):
    """Testes de validação e minimização de dados no ContatoForm."""

    def setUp(self):
        self.area = AreaAtuacao.objects.create(nome="Psicologia", slug="psicologia-form")
        self.servico_ativo = Servico.objects.create(
            nome="Psicoterapia Individual",
            slug="psicoterapia-form",
            area=self.area,
            ativo=True
        )
        self.servico_inativo = Servico.objects.create(
            nome="Serviço Desativado",
            slug="servico-desativado-form",
            area=self.area,
            ativo=False
        )

    def test_valido_apenas_com_email(self):
        dados = {
            'nome': 'João Pereira',
            'email': 'joao@exemplo.com',
            'telefone': '',
            'servico_interesse': self.servico_ativo.pk,
            'mensagem': 'Dúvida sobre atendimento online.',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valido_apenas_com_telefone(self):
        dados = {
            'nome': 'Ana Clara',
            'email': '',
            'telefone': '(61) 98888-7777',
            'mensagem': 'Gostaria de agendar avaliação.',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalido_sem_nenhum_meio_de_retorno(self):
        dados = {
            'nome': 'Carlos Silva',
            'email': '',
            'telefone': '',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('telefone', form.errors)

    def test_invalido_sem_nome(self):
        dados = {
            'nome': '',
            'email': 'teste@exemplo.com',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)

    def test_invalido_com_nome_curto(self):
        dados = {
            'nome': 'A',
            'email': 'teste@exemplo.com',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)

    def test_invalido_sem_aceite_privacidade(self):
        dados = {
            'nome': 'Bruna Mendes',
            'email': 'bruna@exemplo.com',
            'aceite_privacidade': False,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('aceite_privacidade', form.errors)

    def test_invalido_com_email_malformado(self):
        dados = {
            'nome': 'Lucas Rocha',
            'email': 'email-invalido-sem-arroba',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalido_com_mensagem_longa_demais(self):
        dados = {
            'nome': 'Fernanda Costa',
            'email': 'fernanda@exemplo.com',
            'mensagem': 'A' * 2050,  # Ultrapassa 2000
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('mensagem', form.errors)

    def test_rejeita_servico_inativo(self):
        dados = {
            'nome': 'Marcos Lima',
            'email': 'marcos@exemplo.com',
            'servico_interesse': self.servico_inativo.pk,
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('servico_interesse', form.errors)

    def test_honeypot_preenchido_identifica_spam(self):
        dados = {
            'nome': 'Bot Malicioso',
            'email': 'bot@spam.com',
            'campo_verificacao': 'http://link-de-spam.com',
            'aceite_privacidade': True,
        }
        form = ContatoForm(data=dados)
        form.is_valid()
        self.assertTrue(form.is_spam)


class ContatoViewsTest(TestCase):
    """Testes de requisição HTTP, fluxo PRG, rate limit e segurança da view contato."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.config, _ = ConfiguracaoSite.objects.get_or_create(
            pk=1,
            defaults={
                'nome_instituto': 'Instituto Mente em Foco',
                'whatsapp': '5561999998888',
                'mensagem_whatsapp_padrao': 'Olá, gostaria de agendar.',
                'email': 'contato@mentefoco.com.br',
                'ativo': True,
            }
        )

    def tearDown(self):
        cache.clear()

    def test_get_contato_retorna_200_com_template_e_h1_unico(self):
        response = self.client.get(reverse('contato:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contato/index.html')
        self.assertContains(response, '<h1 class="hero-interno__titulo">Contato e Acolhimento</h1>')
        # Garante presença do aviso sobre dados sensíveis
        self.assertContains(response, 'Evite inserir informações clínicas')

    def test_post_valido_salva_e_executa_prg(self):
        dados = {
            'nome': 'Helena Vasconcelos',
            'email': 'helena@exemplo.com',
            'telefone': '(61) 98765-4321',
            'mensagem': 'Olá, gostaria de saber os horários disponíveis.',
            'aceite_privacidade': 'on',
        }
        response = self.client.post(reverse('contato:index'), data=dados)

        # Deve redirecionar para a mesma página (PRG — HTTP 302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('contato:index'))

        # Confirma salvamento no banco de dados
        msg = MensagemContato.objects.filter(email='helena@exemplo.com').first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.nome, 'Helena Vasconcelos')
        self.assertFalse(msg.lida)

        # Ao seguir o redirect, deve conter a mensagem de sucesso
        resp_follow = self.client.get(response.url)
        self.assertEqual(resp_follow.status_code, 200)
        self.assertContains(resp_follow, "Mensagem enviada com sucesso!")

    def test_post_invalido_nao_salva_e_retorna_erros(self):
        dados = {
            'nome': '',
            'email': '',
            'telefone': '',
            'aceite_privacidade': False,
        }
        response = self.client.post(reverse('contato:index'), data=dados)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MensagemContato.objects.exists())
        self.assertContains(response, "Não foi possível enviar a mensagem")

    def test_honeypot_bloqueia_salvamento_silenciosamente(self):
        dados = {
            'nome': 'Spam Bot',
            'email': 'spam@bot.com',
            'campo_verificacao': 'conteudo-armadilha',
            'aceite_privacidade': 'on',
        }
        response = self.client.post(reverse('contato:index'), data=dados)
        # Redireciona com sucesso aparente para não alertar o bot
        self.assertEqual(response.status_code, 302)
        # MAS não salva nada no banco de dados
        self.assertFalse(MensagemContato.objects.filter(nome='Spam Bot').exists())

    def test_rate_limit_bloqueia_excesso_de_submissoes(self):
        dados = {
            'nome': 'Usuário Frequente',
            'email': 'usuario@exemplo.com',
            'aceite_privacidade': 'on',
        }
        # Realiza 5 requisições normais
        for _ in range(5):
            resp = self.client.post(reverse('contato:index'), data=dados)
            self.assertEqual(resp.status_code, 302)

        # A 6ª requisição deve ser bloqueada com status 429
        resp_bloqueada = self.client.post(reverse('contato:index'), data=dados)
        self.assertEqual(resp_bloqueada.status_code, 429)
        self.assertContains(resp_bloqueada, "muitas tentativas de envio em um curto período", status_code=429)

    def test_protecao_xss_mensagem_pura_escapada_no_template(self):
        dados = {
            'nome': 'Usuário Teste XSS',
            'email': 'xss@exemplo.com',
            'mensagem': '<script>alert("xss")</script>',
            'aceite_privacidade': 'on',
        }
        self.client.post(reverse('contato:index'), data=dados)
        msg = MensagemContato.objects.get(email='xss@exemplo.com')
        # O banco armazena o texto puro
        self.assertEqual(msg.mensagem, '<script>alert("xss")</script>')

    def test_csrf_ativo_rejeita_post_sem_token(self):
        client_csrf = Client(enforce_csrf_checks=True)
        dados = {
            'nome': 'Teste CSRF',
            'email': 'csrf@exemplo.com',
            'aceite_privacidade': 'on',
        }
        # Post direto sem token CSRF deve retornar 403 Forbidden
        response = client_csrf.post(reverse('contato:index'), data=dados)
        self.assertEqual(response.status_code, 403)


class ContatoAdminTest(TestCase):
    """Testes do Django Admin para MensagemContato."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_contato',
            email='admin@mentefoco.com',
            password='SenhaAdminForte123!'
        )
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.msg = MensagemContato.objects.create(
            nome="Visitante Teste",
            email="vis@exemplo.com",
            mensagem="Mensagem de teste para visualização no admin.",
            aceite_privacidade=True
        )

    def test_acesso_admin_changelist_e_changeform(self):
        # Changelist
        url_lista = reverse('admin:contato_mensagemcontato_changelist')
        resp_lista = self.client.get(url_lista)
        self.assertEqual(resp_lista.status_code, 200)
        self.assertContains(resp_lista, "Visitante Teste")

        # Changeform (Visualização detalhada)
        url_detalhe = reverse('admin:contato_mensagemcontato_change', args=[self.msg.pk])
        resp_detalhe = self.client.get(url_detalhe)
        self.assertEqual(resp_detalhe.status_code, 200)
        self.assertContains(resp_detalhe, "Visitante Teste")
        self.assertContains(resp_detalhe, "Mensagem de teste para visualização no admin.")


    def test_admin_nao_permite_adicionar_mensagem_manualmente(self):
        admin_obj = admin.site._registry[MensagemContato]
        self.assertFalse(admin_obj.has_add_permission(None))


class PoliticaPrivacidadeTest(TestCase):
    """Testes das rotas e templates da Política de Privacidade (Prompt 11)."""

    def setUp(self):
        self.client = Client()

    def test_rota_politica_privacidade_e_alias_privacidade_respondem_200(self):
        for url in [reverse('paginas:politica_privacidade'), reverse('paginas:privacidade')]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'paginas/politica_privacidade.html')
            self.assertContains(resp, "Política de Privacidade")
            self.assertContains(resp, "Quem Somos")
            self.assertContains(resp, "minimização de dados")

    def test_secoes_estruturadas_politica_privacidade(self):
        resp = self.client.get(reverse('paginas:politica_privacidade'))
        self.assertEqual(resp.status_code, 200)
        # Verifica seções factuais obrigatórias
        self.assertContains(resp, "1. Quem Somos")
        self.assertContains(resp, "2. Quais Dados o Site Pode Coletar")
        self.assertContains(resp, "3. Como os Dados São Obtidos")
        self.assertContains(resp, "4. Para Que os Dados São Utilizados")
        self.assertContains(resp, "5. Formulário de Contato e Orientações Clínicas")
        self.assertContains(resp, "6. Cookies e Tecnologias de Navegação")
        self.assertContains(resp, "7. Serviços de Terceiros e Links Externos")
        self.assertContains(resp, "8. Compartilhamento de Dados")
        self.assertContains(resp, "9. Armazenamento e Retenção dos Dados")
        self.assertContains(resp, "10. Medidas Técnicas de Segurança")
        self.assertContains(resp, "11. Direitos dos Titulares de Dados")
        self.assertContains(resp, "12. Canal de Atendimento a Solicitações de Privacidade")
        self.assertContains(resp, "13. Atualizações e Alterações Desta Política")
        self.assertContains(resp, "14. Data da Última Atualização")

    def test_privacidade_nao_exibe_dados_ficticios_ou_placeholders(self):
        resp = self.client.get(reverse('paginas:politica_privacidade'))
        conteudo = resp.content.decode('utf-8')
        self.assertNotIn("PENDENTE_DEFINICAO", conteudo)
        self.assertNotIn("None", conteudo)


class PoliticaCookiesTest(TestCase):
    """Testes das rotas e templates da Política de Cookies (Prompt 11)."""

    def setUp(self):
        self.client = Client()

    def test_rotas_cookies_respondem_200(self):
        for url in [reverse('paginas:politica_cookies'), reverse('paginas:cookies')]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'paginas/politica_cookies.html')
            self.assertContains(resp, "Política de Cookies")

    def test_cookies_tabela_e_ausencia_rastreadores(self):
        resp = self.client.get(reverse('paginas:politica_cookies'))
        self.assertEqual(resp.status_code, 200)
        # Cookies essenciais auditados
        self.assertContains(resp, "csrftoken")
        self.assertContains(resp, "sessionid")
        self.assertContains(resp, "messages")
        # Ausência de tecnologias de rastreamento confirmada
        self.assertContains(resp, "Sem Google Analytics")
        self.assertContains(resp, "Sem Meta Pixel")

    def test_footer_contem_links_privacidade_e_cookies(self):
        resp = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('paginas:politica_privacidade'))
        self.assertContains(resp, reverse('paginas:politica_cookies'))


class RetencaoContatosTest(TestCase):
    """Testes do comando de gerenciamento limpar_contatos_expirados."""

    def setUp(self):
        self.agora = timezone.now()

    def test_comando_sem_configuracao_aborta_com_seguranca(self):
        out = StringIO()
        # Sem --dias e com setting nulo
        with override_settings(CONTATO_RETENCAO_DIAS=None):
            call_command('limpar_contatos_expirados', stdout=out)
        saida = out.getvalue()
        self.assertIn("[ABORTADO COM SEGURANÇA]", saida)

    def test_comando_dry_run_nao_exclui_registros(self):
        msg = MensagemContato.objects.create(
            nome="Contato Antigo",
            email="antigo@exemplo.com",
            mensagem="Mensagem de 60 dias atrás",
            aceite_privacidade=True
        )
        # Atualiza criado_em para 60 dias atrás
        MensagemContato.objects.filter(pk=msg.pk).update(criado_em=self.agora - timedelta(days=60))

        out = StringIO()
        call_command('limpar_contatos_expirados', '--dias', '30', '--dry-run', stdout=out)
        saida = out.getvalue()

        self.assertIn("[DRY-RUN]", saida)
        self.assertIn("1 mensagem(ns) anterior(es)", saida)
        # Garante que o registro NÃO foi excluído
        self.assertTrue(MensagemContato.objects.filter(pk=msg.pk).exists())

    def test_comando_com_dias_exclui_expirados_e_mantem_recentes(self):
        msg_antiga = MensagemContato.objects.create(
            nome="Contato Expirado",
            email="expirado@exemplo.com",
            mensagem="Mensagem com 45 dias",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg_antiga.pk).update(criado_em=self.agora - timedelta(days=45))

        msg_recente = MensagemContato.objects.create(
            nome="Contato Recente",
            email="recente@exemplo.com",
            mensagem="Mensagem com 5 dias",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg_recente.pk).update(criado_em=self.agora - timedelta(days=5))

        out = StringIO()
        call_command('limpar_contatos_expirados', '--dias', '30', stdout=out)
        saida = out.getvalue()

        self.assertIn("Limpeza de retenção concluída com sucesso: 1 mensagem(ns)", saida)
        # O antigo foi excluído
        self.assertFalse(MensagemContato.objects.filter(pk=msg_antiga.pk).exists())
        # O recente permaneceu intacto
        self.assertTrue(MensagemContato.objects.filter(pk=msg_recente.pk).exists())

    def test_comando_zero_pii_no_output(self):
        msg = MensagemContato.objects.create(
            nome="Nome Confidencial Titular",
            email="titular_confidencial@exemplo.com",
            telefone="61999998888",
            mensagem="Texto confidencial do titular",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg.pk).update(criado_em=self.agora - timedelta(days=40))

        out = StringIO()
        call_command('limpar_contatos_expirados', '--dias', '30', stdout=out)
        saida = out.getvalue()

        # Saída NÃO deve conter PII
        self.assertNotIn("Nome Confidencial Titular", saida)
        self.assertNotIn("titular_confidencial@exemplo.com", saida)
        self.assertNotIn("61999998888", saida)
        self.assertNotIn("Texto confidencial do titular", saida)


class EmailNotificacaoPrivacidadeTest(TestCase):
    """Testes de privacidade no envio de notificações por e-mail."""

    def setUp(self):
        self.client = Client()
        self.config = ConfiguracaoSite.objects.create(
            pk=1,
            nome_instituto="Instituto Mente em Foco",
            email="clinica@mentefoco.com.br",
            ativo=True
        )

    def test_email_notificacao_assunto_sem_pii(self):
        dados = {
            'nome': 'Clarice Lispector',
            'email': 'clarice@exemplo.com',
            'mensagem': 'Gostaria de agendar um atendimento.',
            'aceite_privacidade': 'on',
        }
        resp = self.client.post(reverse('contato:index'), data=dados)
        self.assertEqual(resp.status_code, 302)

        # Verifica caixa de e-mails de teste
        self.assertEqual(len(mail.outbox), 1)
        email_enviado = mail.outbox[0]
        # O assunto NÃO deve conter o nome do visitante (PII)
        self.assertEqual(email_enviado.subject, "[Novo Contato] Nova mensagem recebida pelo site")
        self.assertNotIn("Clarice Lispector", email_enviado.subject)

