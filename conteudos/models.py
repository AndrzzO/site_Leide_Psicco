"""
Modelos do app conteudos:
- CategoriaArtigo: Categorias temáticas editoriais para classificação de artigos.
- Artigo: Publicações educativas e informativas do Blog com controle de rascunho/publicação.
"""
import math
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
from nucleo.validators import validar_imagem
from nucleo.upload_paths import caminho_upload_artigo
from .sanitizacao import renderizar_markdown_seguro


class CategoriaArtigo(models.Model):
    """
    Categoria temática editorial do Blog (ex: Psicologia Clínica, Relacionamentos,
    Traumas e Recomeços, Neuropsicologia e Avaliação).
    """
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Categoria",
        help_text="Ex: Psicologia Clínica, Relacionamentos, Neuropsicologia."
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name="Slug da URL",
        help_text="Identificador único da categoria na URL."
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição da Categoria",
        help_text="Breve contextualização editorial sobre os temas desta categoria."
    )
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordem de Exibição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Categorias inativas não aparecem nos filtros públicos."
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Categoria de Artigo"
        verbose_name_plural = "Categorias de Artigos"
        ordering = ['ordem', 'nome']

    def save(self, *args, **kwargs):
        """Gera slug seguro na criação e preserva a estabilidade nas atualizações."""
        if not self.slug:
            slug_base = slugify(self.nome)
            slug_candidato = slug_base
            contador = 1
            while CategoriaArtigo.objects.filter(slug=slug_candidato).exclude(pk=self.pk).exists():
                slug_candidato = f"{slug_base}-{contador}"
                contador += 1
            self.slug = slug_candidato
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ArtigoQuerySet(models.QuerySet):
    """QuerySet customizado para consultas públicas seguras de artigos."""

    def publicados(self):
        """
        Retorna exclusivamente artigos com status 'publicado',
        cuja data de publicação já tenha sido atingida (<= agora)
        e cuja categoria seja ativa ou nula.
        """
        agora = timezone.now()
        return self.filter(
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao__lte=agora
        ).filter(
            models.Q(categoria__isnull=True) | models.Q(categoria__ativo=True)
        )


class Artigo(models.Model):
    """
    Artigo educativo e institucional do Instituto Mente em Foco.
    Suporta ciclo de vida editorial (Rascunho / Publicado), agendamento futuro,
    renderização sanitizada de Markdown e SEO básico.
    """
    STATUS_RASCUNHO = 'rascunho'
    STATUS_PUBLICADO = 'publicado'
    STATUS_CHOICES = [
        (STATUS_RASCUNHO, 'Rascunho'),
        (STATUS_PUBLICADO, 'Publicado'),
    ]

    titulo = models.CharField(
        max_length=200,
        verbose_name="Título do Artigo",
        help_text="Título claro e informativo para leitores e buscadores."
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="Slug da URL",
        help_text="Identificador único na URL. Gerado automaticamente na criação; evite alterar após publicado."
    )
    resumo = models.TextField(
        blank=True,
        verbose_name="Resumo / Linha Fina",
        help_text="Resumo conciso exibido nos cards da listagem e da Home."
    )
    conteudo = models.TextField(
        blank=True,
        verbose_name="Conteúdo (Markdown)",
        help_text="Texto do artigo formatado em Markdown seguro. Use ## para subtítulos (H2). Tags script e H1 são bloqueadas."
    )
    imagem_capa = models.ImageField(
        upload_to=caminho_upload_artigo,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Imagem de Capa",
        help_text="Proporção recomendada: ~16:9. Formatos suportados: JPG, PNG, WEBP."
    )
    texto_alternativo_imagem = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Texto Alternativo da Capa (alt)",
        help_text="Descreva objetivamente a imagem para leitores de tela e acessibilidade."
    )
    categoria = models.ForeignKey(
        CategoriaArtigo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artigos',
        verbose_name="Categoria"
    )
    autor = models.ForeignKey(
        'nucleo.Profissional',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artigos',
        verbose_name="Autor(a)",
        help_text="Profissional responsável pela autoria do texto. Deixe vazio se não houver autoria confirmada."
    )
    servico_relacionado = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artigos_relacionados',
        verbose_name="Serviço Relacionado",
        help_text="Serviço do Instituto vinculado ao tema do artigo para direcionamento de leitura."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_RASCUNHO,
        verbose_name="Status Editorial",
        help_text="Apenas artigos 'Publicados' com data <= agora aparecem publicamente no site."
    )
    destaque = models.BooleanField(
        default=False,
        verbose_name="Destaque Principal na Listagem",
        help_text="Se marcado, será exibido no topo da página de Conteúdos."
    )
    data_publicacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Publicação",
        help_text="Se o status for 'Publicado' e este campo estiver vazio, será preenchido com a data/hora atual."
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    # Metadados Básicos para SEO
    meta_titulo = models.CharField(
        max_length=70,
        blank=True,
        verbose_name="Meta Title (SEO)",
        help_text="Título conciso para buscadores (ideal até ~60-70 caracteres). Deixe vazio para usar o título do artigo."
    )
    meta_descricao = models.TextField(
        blank=True,
        verbose_name="Meta Description (SEO)",
        help_text="Resumo utilizado por mecanismos de busca (ideal entre 140 e 160 caracteres). Deixe vazio para usar o resumo."
    )

    objects = ArtigoQuerySet.as_manager()

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-data_publicacao', '-data_criacao']

    def save(self, *args, **kwargs):
        """
        1. Gera slug único e estável na criação.
        2. Preenche data_publicacao automaticamente com timezone.now() se o artigo
           for definido como publicado e a data estiver vazia.
        """
        if not self.slug:
            slug_base = slugify(self.titulo)
            slug_candidato = slug_base
            contador = 1
            while Artigo.objects.filter(slug=slug_candidato).exclude(pk=self.pk).exists():
                slug_candidato = f"{slug_base}-{contador}"
                contador += 1
            self.slug = slug_candidato

        if self.status == self.STATUS_PUBLICADO and not self.data_publicacao:
            self.data_publicacao = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Retorna a URL pública canônica do artigo."""
        return reverse('conteudos:detalhe', kwargs={'slug': self.slug})

    @property
    def conteudo_formatado(self):
        """Retorna o conteúdo formatado em HTML seguro e rigorosamente sanitizado via Bleach."""
        return renderizar_markdown_seguro(self.conteudo)

    @property
    def tempo_leitura_minutos(self):
        """Calcula o tempo estimado de leitura (base média de 200 palavras por minuto)."""
        texto_puro = strip_tags(self.conteudo_formatado)
        palavras = len(texto_puro.split())
        return max(1, math.ceil(palavras / 200))

    def __str__(self):
        return self.titulo
