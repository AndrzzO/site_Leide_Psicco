"""
Modelos do app servicos:
- AreaAtuacao: Grandes áreas clínicas e estruturais (Home e páginas institucionais).
- Servico: Serviços específicos, psicoterapias, avaliações e reabilitações.
"""
from django.db import models
from django.utils.text import slugify
from nucleo.validators import validar_imagem
from nucleo.upload_paths import caminho_upload_area, caminho_upload_servico


class AreaAtuacao(models.Model):
    """
    Áreas de atuação e pilares fundamentais do Instituto Mente em Foco.
    Utilizadas nos cards de identificação e navegação principal.
    """
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome da Área",
        help_text="Ex: Psicologia, Neuropsicologia, Traumas, Separação e Recomeços, Novos Relacionamentos"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        verbose_name="Slug da URL"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título Editorial",
        help_text="Título exibido em destaque nos cards e cabeçalhos"
    )
    resumo = models.TextField(
        verbose_name="Resumo Curto",
        help_text="Texto conciso exibido nos cards da página inicial."
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição Completa da Área"
    )
    imagem = models.ImageField(
        upload_to=caminho_upload_area,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Fotografia do Card",
        help_text="Proporção recomendada: ~4:3."
    )
    texto_alternativo_imagem = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Texto Alternativo da Imagem (alt)",
        help_text="Descreva objetivamente o conteúdo relevante da fotografia para acessibilidade."
    )
    frase_destaque = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Frase de Destaque / Citação"
    )
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordem de Exibição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    mostrar_na_home = models.BooleanField(
        default=True,
        verbose_name="Mostrar na Página Inicial"
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
        verbose_name = "Área de Atuação"
        verbose_name_plural = "Áreas de Atuação"
        ordering = ['ordem', 'nome']

    def save(self, *args, **kwargs):
        """Gera slug seguro a partir do nome se ainda não estiver preenchido."""
        if not self.slug:
            slug_base = slugify(self.nome)
            slug_candidato = slug_base
            contador = 1
            while AreaAtuacao.objects.filter(slug=slug_candidato).exclude(pk=self.pk).exists():
                slug_candidato = f"{slug_base}-{contador}"
                contador += 1
            self.slug = slug_candidato
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    """
    Serviços clínicos, avaliativos e terapêuticos oferecidos pelo Instituto.
    """
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome do Serviço"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        verbose_name="Slug da URL"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título da Página"
    )
    subtitulo = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Subtítulo"
    )
    resumo = models.TextField(
        verbose_name="Resumo Explicativo",
        help_text="Apresentação inicial acolhedora da atuação."
    )
    descricao = models.TextField(
        verbose_name="Descrição Detalhada do Atendimento",
        help_text="Texto explicativo estruturado, sem jargões excessivos e sem promessas de cura."
    )
    frase_destaque = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Frase de Destaque"
    )
    area = models.ForeignKey(
        AreaAtuacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servicos',
        verbose_name="Área de Atuação Relacionada"
    )
    imagem_principal = models.ImageField(
        upload_to=caminho_upload_servico,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Imagem Principal da Página",
        help_text="Proporção recomendada: ~16:9."
    )
    texto_alternativo_imagem = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Texto Alternativo da Imagem (alt)"
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Identificador do Ícone",
        help_text="Ex: cerebro, perfil, prancheta, flor"
    )
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordem de Exibição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    mostrar_na_home = models.BooleanField(
        default=True,
        verbose_name="Mostrar na Página Inicial"
    )

    # Metadados Básicos para SEO
    meta_titulo = models.CharField(
        max_length=70,
        blank=True,
        verbose_name="Meta Title (SEO)",
        help_text="Título conciso para buscadores (ideal até ~60-70 caracteres)."
    )
    meta_descricao = models.TextField(
        blank=True,
        verbose_name="Meta Description (SEO)",
        help_text="Resumo utilizado por mecanismos de busca (ideal entre 140 e 160 caracteres)."
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
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['ordem', 'nome']

    def save(self, *args, **kwargs):
        """Gera slug seguro a partir do nome se ainda não preenchido."""
        if not self.slug:
            slug_base = slugify(self.nome)
            slug_candidato = slug_base
            contador = 1
            while Servico.objects.filter(slug=slug_candidato).exclude(pk=self.pk).exists():
                slug_candidato = f"{slug_base}-{contador}"
                contador += 1
            self.slug = slug_candidato
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
