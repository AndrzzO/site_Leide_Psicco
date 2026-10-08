"""
Modelos centrais do Instituto Mente em Foco:
- ConfiguracaoSite: Singleton para dados institucionais, canais de contato e identidade.
- Profissional: Apresentação da Psicóloga Mari Menezes.
- RedeSocial: Canais oficiais externos.
"""
import urllib.parse
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .validators import validar_imagem
from .upload_paths import caminho_upload_institucional, caminho_upload_profissional


class ConfiguracaoSite(models.Model):
    """
    Configuração global do site institucional (Padrão Singleton).
    Centraliza as informações gerais do Instituto, garantindo um único registro ativo.
    """
    nome_instituto = models.CharField(
        max_length=150,
        default="Instituto Mente em Foco",
        verbose_name="Nome do Instituto"
    )
    razao_social = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Razão Social / Nome Jurídico"
    )
    slogan_principal = models.CharField(
        max_length=255,
        default="COMPREENDER • CUIDAR • RECONSTRUIR",
        verbose_name="Conceito / Slogan Principal"
    )
    frase_institucional = models.TextField(
        default=(
            "Psicologia e Neuropsicologia para compreender a mente, "
            "cuidar das emoções e construir novos caminhos."
        ),
        verbose_name="Frase Institucional"
    )
    frase_emocional = models.CharField(
        max_length=255,
        default="Sua história merece ser compreendida.",
        verbose_name="Frase Emocional"
    )
    cta_principal = models.CharField(
        max_length=100,
        default="Comece por você.",
        verbose_name="CTA Institucional Principal"
    )
    mensagem_whatsapp_padrao = models.TextField(
        default=(
            "Olá, Mari. Conheci o Instituto Mente em Foco pelo site e "
            "gostaria de informações sobre o atendimento psicológico/neuropsicológico."
        ),
        verbose_name="Mensagem Padrão do WhatsApp"
    )

    # Contato e Atendimento
    telefone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Telefone Fixo"
    )
    whatsapp = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="WhatsApp Comercial",
        help_text="Somente números com código do país e DDD (Ex: 5561999999999)"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail de Contato"
    )
    instagram = models.URLField(
        blank=True,
        verbose_name="Link do Instagram Oficial"
    )

    # Localização e Horários
    endereco_texto = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Endereço Completo"
    )
    modalidade_atendimento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Modalidade de Atendimento",
        help_text="Ex: Presencial, Online ou Híbrido"
    )
    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Estado (UF)"
    )
    mapa_url = models.URLField(
        blank=True,
        verbose_name="Link do Google Maps"
    )
    horario_atendimento = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Horário de Atendimento"
    )

    # Identidade Visual e Imagens Institucionais
    logo = models.ImageField(
        upload_to=caminho_upload_institucional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Logotipo Principal"
    )
    logo_horizontal = models.ImageField(
        upload_to=caminho_upload_institucional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Logotipo Horizontal"
    )
    logo_vertical = models.ImageField(
        upload_to=caminho_upload_institucional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Logotipo Vertical"
    )
    favicon = models.ImageField(
        upload_to=caminho_upload_institucional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Favicon (Ícone de Navegador)"
    )
    imagem_compartilhamento_padrao = models.ImageField(
        upload_to=caminho_upload_institucional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Imagem Padrão Open Graph (1200x630)"
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configuração do Site"

    def clean(self):
        """Impede criação de múltiplos registros garantindo padrão Singleton."""
        if not self.pk and ConfiguracaoSite.objects.exists():
            raise ValidationError("Já existe uma configuração do site cadastrada. Edite o registro existente.")

    def save(self, *args, **kwargs):
        """Garante que a chave primária seja sempre 1."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Retorna o registro único de configuração ou cria um com valores padrão."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        """Gera o link seguro para abertura direta de conversa no WhatsApp."""
        if not self.whatsapp:
            return ""
        numero_limpo = "".join(filter(str.isdigit, str(self.whatsapp)))
        if not numero_limpo:
            return ""
        mensagem = urllib.parse.quote(self.mensagem_whatsapp_padrao or "")
        return f"https://wa.me/{numero_limpo}?text={mensagem}"

    def __str__(self):
        return self.nome_instituto


class Profissional(models.Model):
    """
    Cadastro profissional da Psicóloga Mari Menezes.
    Permite gerenciar biografia, qualificações reais e fotografias editoriais.
    """
    nome = models.CharField(
        max_length=150,
        default="Mari Menezes",
        verbose_name="Nome Completo"
    )
    nome_exibicao = models.CharField(
        max_length=100,
        default="Psicóloga Mari Menezes",
        verbose_name="Nome de Exibição"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        verbose_name="Identificador da URL (Slug)"
    )
    titulo_profissional = models.CharField(
        max_length=200,
        default="Psicóloga, palestrante e facilitadora de grupos",
        verbose_name="Título Profissional"
    )
    atuacao_resumida = models.CharField(
        max_length=200,
        default="Psicologia e Neuropsicologia",
        verbose_name="Área de Atuação Principal"
    )
    biografia_curta = models.TextField(
        default=(
            "Minha prática parte da compreensão de que cada pessoa carrega "
            "uma história que precisa ser compreendida antes de ser julgada. "
            "Meu trabalho busca oferecer um espaço de escuta profissional, "
            "acolhimento e construção de estratégias para diferentes momentos da vida."
        ),
        verbose_name="Biografia Curta / Apresentação"
    )
    biografia_completa = models.TextField(
        blank=True,
        verbose_name="Biografia Completa",
        help_text="Texto detalhado da trajetória profissional para a página Sobre Mim."
    )
    frase_destaque = models.CharField(
        max_length=255,
        default="Meu propósito é ajudar pessoas a compreenderem melhor a própria história e encontrarem recursos para seguir seus caminhos.",
        verbose_name="Frase de Destaque"
    )
    registro_profissional = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Registro Profissional (CRP)",
        help_text="Número oficial do CRP com região (Ex: CRP 00/00000). Deixar vazio se pendente."
    )
    formacao_resumida = models.TextField(
        blank=True,
        verbose_name="Formação e Qualificações Reais",
        help_text="Inserir somente graduações, especializações e títulos acadêmicos reais comprovados."
    )

    # Fotografias Editoriais
    foto_principal = models.ImageField(
        upload_to=caminho_upload_profissional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Fotografia Principal (Hero)",
        help_text="Proporção recomendada: vertical ~4:5."
    )
    foto_sobre = models.ImageField(
        upload_to=caminho_upload_profissional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Fotografia para Seção Sobre Mim",
        help_text="Proporção recomendada: vertical ~4:5."
    )
    foto_secundaria = models.ImageField(
        upload_to=caminho_upload_profissional,
        blank=True,
        null=True,
        validators=[validar_imagem],
        verbose_name="Fotografia Secundária / Ambiente"
    )

    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordem de Exibição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    destaque = models.BooleanField(
        default=True,
        verbose_name="Destaque na Página Inicial"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ['ordem', 'nome']

    def save(self, *args, **kwargs):
        """Gera slug seguro a partir do nome na criação, preservando-o em edições."""
        if not self.slug:
            slug_base = slugify(self.nome)
            slug_candidato = slug_base
            contador = 1
            while Profissional.objects.filter(slug=slug_candidato).exclude(pk=self.pk).exists():
                slug_candidato = f"{slug_base}-{contador}"
                contador += 1
            self.slug = slug_candidato
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_exibicao} ({self.titulo_profissional})"


class RedeSocial(models.Model):
    """
    Redes sociais e canais oficiais externos do Instituto.
    """
    ICONE_CHOICES = [
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(
        max_length=50,
        verbose_name="Nome da Rede"
    )
    url = models.URLField(
        verbose_name="Link do Perfil"
    )
    icone = models.CharField(
        max_length=50,
        choices=ICONE_CHOICES,
        default='instagram',
        verbose_name="Identificador do Ícone"
    )
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordem de Exibição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        verbose_name = "Rede Social"
        verbose_name_plural = "Redes Sociais"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.url})"


class BloqueioLogin(models.Model):
    """Estado durável compartilhado pelos dois logins, sem armazenar o IP em claro."""
    origem = models.CharField(max_length=32, unique=True)
    falhas = models.PositiveIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=0)
    bloqueado_ate = models.DateTimeField(null=True, blank=True)
    permanente = models.BooleanField(default=False)
    reserva_ate = models.DateTimeField(null=True, blank=True)
    reserva_token = models.CharField(max_length=32, blank=True)
