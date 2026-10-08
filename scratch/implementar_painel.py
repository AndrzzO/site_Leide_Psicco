from pathlib import Path
p=Path('conteudos/models.py'); s=p.read_text(encoding='utf-8-sig'); s=s.replace('data_publicacao__lte=agora\n','data_publicacao__lte=agora\n').replace('models.Q(categoria__isnull=True) | models.Q(categoria__ativo=True)\n        )','models.Q(categoria__isnull=True) | models.Q(categoria__ativo=True)\n        ).filter(models.Q(apagar_em__isnull=True) | models.Q(apagar_em__gt=agora))')
s=s.replace('    titulo = models.CharField(','''    FONTES = [('montserrat', 'Montserrat'), ('georgia', 'Georgia'), ('arial', 'Arial'), ('palatino', 'Palatino')]
    fonte = models.CharField(max_length=20, choices=FONTES, default='montserrat')
    apagar_em = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Apagar automaticamente em')
    formato_html = models.BooleanField(default=False, editable=False)

    titulo = models.CharField(''',1)
s=s.replace('        ordering = [\'-data_publicacao\', \'-data_criacao\']',"        ordering = ['-data_publicacao', '-data_criacao']\n        permissions = [('gerenciar_blog', 'Pode gerenciar o Blog pelo painel reservado')]")
s=s.replace('        return renderizar_markdown_seguro(self.conteudo)',"        if self.formato_html:\n            from .sanitizacao import sanitizar_editor\n            return sanitizar_editor(self.conteudo)\n        return renderizar_markdown_seguro(self.conteudo)")
p.write_text(s,encoding='utf-8')
p=Path('conteudos/sanitizacao.py'); p.write_text(p.read_text(encoding='utf-8-sig')+'''

def sanitizar_editor(html):
    return bleach.clean(html or '', tags=['p', 'div', 'br', 'h2', 'h3', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'blockquote', 'a'], attributes={'a': ['href', 'title']}, protocols=['https', 'http', 'mailto'], strip=True)
''',encoding='utf-8')
p=Path('nucleo/models.py'); p.write_text(p.read_text(encoding='utf-8-sig')+'''

class BloqueioLogin(models.Model):
    """Estado durável compartilhado pelos dois logins, sem armazenar o IP em claro."""
    origem = models.CharField(max_length=32, unique=True)
    falhas = models.PositiveIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=0)
    bloqueado_ate = models.DateTimeField(null=True, blank=True)
    permanente = models.BooleanField(default=False)
    reserva_ate = models.DateTimeField(null=True, blank=True)
    reserva_token = models.CharField(max_length=32, blank=True)
''',encoding='utf-8')
p=Path('nucleo/rate_limit.py'); s=p.read_text(encoding='utf-8-sig'); s=s[:s.index('    @classmethod\n    def verificar_login_ip')]+'''\n\ndef wrap_admin_login(admin_site):
    if getattr(admin_site, '_rate_limit_wrapped', False):
        return
    from .login_security import proteger_login
    admin_site.login = proteger_login(admin_site.login)
    admin_site._rate_limit_wrapped = True
'''; p.write_text(s,encoding='utf-8')
p=Path('configuracoes/urls.py');s=p.read_text(encoding='utf-8-sig').replace("    path('conteudos/',", "    path('area-cliente/', include('conteudos.painel_urls')),\n    path('conteudos/',");p.write_text(s,encoding='utf-8')
p=Path('templates/componentes/footer.html');s=p.read_text(encoding='utf-8-sig').replace('<li><a href="{% url \'paginas:politica_cookies\' %}">Política de Cookies</a></li>', '<li><a href="{% url \'paginas:politica_cookies\' %}">Política de Cookies</a></li>\n                        <li class="footer-acesso"><a href="{% url \'painel:login\' %}" rel="nofollow">Área reservada</a></li>');p.write_text(s,encoding='utf-8')
p=Path('templates/conteudos/detalhe.html');s=p.read_text(encoding='utf-8-sig').replace('class="artigo-corpo-leitura"','class="artigo-corpo-leitura fonte-{{ artigo.fonte }}"');p.write_text(s,encoding='utf-8')
p=Path('nucleo/sitemaps.py');s=p.read_text(encoding='utf-8-sig').replace('artigos__status=Artigo.STATUS_PUBLICADO,\n            artigos__data_publicacao__lte=agora','artigos__in=Artigo.objects.publicados()');p.write_text(s,encoding='utf-8')
p=Path('conteudos/admin.py');s=p.read_text(encoding='utf-8-sig').replace('"data_publicacao",','"data_publicacao",\n                "apagar_em",').replace('"conteudo",','"conteudo",\n                "fonte",');p.write_text(s,encoding='utf-8')
