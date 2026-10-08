from pathlib import Path
p=Path('conteudos/models.py');s=p.read_text(encoding='utf-8-sig');marker='    def get_absolute_url(self):';insert='''    @property
    def situacao_publica(self):
        agora = timezone.now()
        if self.apagar_em and self.apagar_em <= agora:
            return 'Expirado'
        if self.status != self.STATUS_PUBLICADO:
            return 'Rascunho'
        if not self.data_publicacao or self.data_publicacao > agora:
            return 'Agendado'
        if self.categoria_id and not self.categoria.ativo:
            return 'Categoria inativa'
        return 'Publicado'

    @property
    def visivel_no_site(self):
        return self.situacao_publica == 'Publicado'

''';s=s.replace(marker,insert+marker);p.write_text(s,encoding='utf-8')
p=Path('templates/conteudos/painel/index.html');s=p.read_text(encoding='utf-8-sig').replace('{{ artigo.get_status_display }}','{{ artigo.situacao_publica }}').replace("{% if artigo.status == 'publicado' %}",'{% if artigo.visivel_no_site %}');s=s.replace('<h2>{{ artigo.titulo }}</h2>', '''<h2>{{ artigo.titulo }}</h2>{% if artigo.situacao_publica == 'Expirado' %}<p>O prazo terminou e este artigo não está mais no site. Para republicar, edite e escolha “Permanente” ou uma nova data.</p>{% elif artigo.situacao_publica == 'Categoria inativa' %}<p>Escolha uma categoria ativa na edição para exibir este artigo.</p>{% elif artigo.situacao_publica == 'Agendado' %}<p>Disponível a partir de {{ artigo.data_publicacao|date:'d/m/Y à\\s H:i' }}.</p>{% endif %}''');p.write_text(s,encoding='utf-8')
p=Path('conteudos/tests_painel.py');s=p.read_text(encoding='utf-8-sig');s+='''
    def test_painel_nao_oferece_link_para_artigo_expirado_e_permite_republicar(self):
        self.client.force_login(self.user)
        artigo = Artigo.objects.create(titulo='Prazo terminado', status='publicado', apagar_em=timezone.now()-timedelta(days=1))
        response = self.client.get(reverse('painel:index'))
        self.assertContains(response, 'Expirado')
        self.assertNotContains(response, 'Ver no site')
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 404)
        self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados)
        artigo.refresh_from_db()
        self.assertIsNone(artigo.apagar_em)
        self.assertContains(self.client.get(reverse('painel:index')), 'Ver no site')
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 200)

    def test_situacao_publica_respeita_agendamento_e_categoria(self):
        categoria = CategoriaArtigo.objects.create(nome='Oculta', ativo=False)
        artigo = Artigo.objects.create(titulo='Teste de situação', status='publicado', categoria=categoria)
        self.assertFalse(artigo.visivel_no_site)
        self.assertEqual(artigo.situacao_publica, 'Categoria inativa')
        artigo.categoria = None
        artigo.data_publicacao = timezone.now()+timedelta(days=1)
        self.assertEqual(artigo.situacao_publica, 'Agendado')
        self.assertFalse(artigo.visivel_no_site)
''';p.write_text(s,encoding='utf-8')
