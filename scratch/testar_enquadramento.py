from pathlib import Path
p=Path('static/js/enquadramento-capa.js');s=p.read_text(encoding='utf-8-sig').replace('    image.style.objectPosition = `${x.value || 50}% ${y.value || 50}%`;\n    // Zero é uma posição válida.\n','');p.write_text(s,encoding='utf-8')
p=Path('conteudos/tests_painel.py');s=p.read_text(encoding='utf-8-sig');s+='''
    def test_enquadramento_persiste_e_rejeita_valores_invalidos(self):
        self.client.force_login(self.user)
        self.client.post(reverse('painel:novo'), {**self.dados, 'capa_x': '0', 'capa_y': '83'})
        artigo = Artigo.objects.get()
        self.assertEqual((artigo.capa_x, artigo.capa_y), (0, 83))
        form = ArtigoEditorForm(instance=artigo)
        self.assertEqual(form['capa_y'].value(), 83)
        for valor in ['-1', '101', '50; color:red', 'abc']:
            form = ArtigoEditorForm({**self.dados, 'capa_x': valor})
            self.assertFalse(form.is_valid())
        self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados)
        artigo.refresh_from_db()
        self.assertEqual((artigo.capa_x, artigo.capa_y), (0, 83))
''';p.write_text(s,encoding='utf-8')
