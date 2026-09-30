"""
Definição dos sitemaps XML para o Instituto Mente em Foco utilizando django.contrib.sitemaps.
Inclui rotas públicas canônicas e exclui rigorosamente painel administrativo,
health check, páginas privadas, rascunhos e busca interna.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from servicos.models import Servico
from conteudos.models import Artigo, CategoriaArtigo


class ItemPaginaEstatica:
    """Representa uma página institucional fixa para o sitemap."""
    def __init__(self, url_name, priority, changefreq, lastmod=None):
        self.url_name = url_name
        self.priority = priority
        self.changefreq = changefreq
        self.lastmod = lastmod


class PaginasSitemap(Sitemap):
    """
    Sitemap para páginas institucionais fixas do Instituto Mente em Foco.
    """
    protocol = 'https'

    def items(self):
        return [
            ItemPaginaEstatica('paginas:inicio', 1.0, 'weekly'),
            ItemPaginaEstatica('paginas:credenciamento', 0.6, 'monthly'),
            ItemPaginaEstatica('paginas:sobre_mim', 0.8, 'monthly'),
            ItemPaginaEstatica('contato:index', 0.8, 'monthly'),
            ItemPaginaEstatica('paginas:politica_privacidade', 0.3, 'yearly'),
            ItemPaginaEstatica('paginas:politica_cookies', 0.3, 'yearly'),
        ]

    def location(self, obj):
        return reverse(obj.url_name)

    def priority(self, obj):
        return obj.priority

    def changefreq(self, obj):
        return obj.changefreq

    def lastmod(self, obj):
        return obj.lastmod


class ItemServicoSitemap:
    """Representa uma página de serviço clínico com URL reversa e metadados."""
    def __init__(self, url_name, slug=None, priority=0.8, changefreq='monthly'):
        self.url_name = url_name
        self.slug = slug
        self.priority = priority
        self.changefreq = changefreq

    @property
    def servico_obj(self):
        if not hasattr(self, '_cached_servico'):
            self._cached_servico = (
                Servico.objects.filter(slug=self.slug, ativo=True).first()
                if self.slug else None
            )
        return self._cached_servico

    @property
    def lastmod(self):
        if self.servico_obj:
            return self.servico_obj.data_atualizacao
        return None


class ServicosSitemap(Sitemap):
    """
    Sitemap para todas as páginas de serviços clínicos, avaliações e psicoterapias.
    Exclui serviços inativos.
    """
    protocol = 'https'

    def items(self):
        # Mapeia as URLs de serviços aos seus respectivos slugs de banco para extração do lastmod
        servicos_config = [
            ItemServicoSitemap('servicos:psicologia', 'psicologia-clinica', priority=0.9),
            ItemServicoSitemap('servicos:neuropsicologia', 'neuropsicologia-clinica', priority=0.9),
            ItemServicoSitemap('servicos:traumas', 'acompanhamento-traumas', priority=0.8),
            ItemServicoSitemap('servicos:separacao_recomecos', 'atendimento-separacao', priority=0.8),
            ItemServicoSitemap('servicos:novos_relacionamentos', 'novos-relacionamentos-atendimento', priority=0.8),
            ItemServicoSitemap('servicos:avaliacao', None, priority=0.8),
            ItemServicoSitemap('servicos:avaliacao_psicologica', 'avaliacao-psicologica', priority=0.8),
            ItemServicoSitemap('servicos:avaliacao_neuropsicologica', 'avaliacao-neuropsicologica', priority=0.8),
            ItemServicoSitemap('servicos:reabilitacao_neurocognitiva', 'reabilitacao-neurocognitiva', priority=0.8),
        ]

        # Retorna apenas serviços que não estejam explicitamente inativos no banco
        itens_validos = []
        for item in servicos_config:
            if item.slug:
                servico = Servico.objects.filter(slug=item.slug).first()
                if servico and not servico.ativo:
                    continue  # Pula serviço inativo
            itens_validos.append(item)
        return itens_validos

    def location(self, obj):
        return reverse(obj.url_name)

    def priority(self, obj):
        return obj.priority

    def changefreq(self, obj):
        return obj.changefreq

    def lastmod(self, obj):
        return obj.lastmod


class ConteudosSitemap(Sitemap):
    """
    Sitemap para artigos publicados do Blog educativo.
    Inclui estritamente artigos publicados com data <= agora e categoria ativa.
    """
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Artigo.objects.publicados().select_related('categoria', 'autor')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.data_atualizacao


class CategoriasSitemap(Sitemap):
    """
    Sitemap para páginas de categorias ativas do Blog que contenham artigos publicados.
    """
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        agora = timezone.now()
        return CategoriaArtigo.objects.filter(
            ativo=True,
            artigos__status=Artigo.STATUS_PUBLICADO,
            artigos__data_publicacao__lte=agora
        ).distinct()

    def location(self, obj):
        return reverse('conteudos:categoria', kwargs={'categoria_slug': obj.slug})

    def lastmod(self, obj):
        return obj.data_atualizacao


class AvaliacoesEspecificasSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        from servicos.editorial import AVALIACOES
        return [item['slug'] for item in AVALIACOES]

    def location(self, slug):
        return reverse('servicos:avaliacao_especifica', kwargs={'slug': slug})


sitemaps = {
    'avaliacoes_especificas': AvaliacoesEspecificasSitemap(),
    'paginas': PaginasSitemap,
    'servicos': ServicosSitemap,
    'conteudos': ConteudosSitemap,
    'categorias': CategoriasSitemap,
}
