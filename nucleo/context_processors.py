"""
Context processors globais do Instituto Mente em Foco.
Injeta dados institucionais a partir do model ConfiguracaoSite ou fallbacks seguros.
"""
import urllib.parse
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError


def dados_institucionais(request):
    """
    Retorna o contexto global com informações da marca a partir do banco de dados,
    com suporte a fallbacks seguros caso a tabela ainda não tenha sido migrada ou o registro não exista.
    """
    # Valores padrão de fallback seguros
    nome_instituto = "Instituto Mente em Foco"
    nome_profissional = "Psicóloga Mari Menezes"
    conceito_triplice = "COMPREENDER • CUIDAR • RECONSTRUIR"
    assinatura_institucional = (
        "Avaliações psicológicas, laudos, pareceres e relatórios. "
        "Psicoterapia com responsabilidade e acolhimento."
    )
    assinatura_emocional = "Sua história merece ser compreendida."
    mensagem_rodape = "Cuidar da mente também é uma forma de recomeçar."
    mensagem_whatsapp = (
        "Olá, Mari. Conheci o Instituto Mente em Foco pelo site e "
        "gostaria de informações sobre o atendimento psicológico/neuropsicológico."
    )
    whatsapp_numero = getattr(settings, 'WHATSAPP_NUMERO', 'PENDENTE_DEFINICAO')
    email_contato = getattr(settings, 'EMAIL_CONTATO', 'PENDENTE_DEFINICAO')
    instagram_url = getattr(settings, 'INSTAGRAM_URL', 'PENDENTE_DEFINICAO')
    crp_profissional = getattr(settings, 'CRP_PROFISSIONAL', 'PENDENTE_DEFINICAO')
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    whatsapp_link = ""
    config_obj = None
    redes_sociais = []

    # Tenta consultar o banco de forma resiliente
    try:
        from .models import ConfiguracaoSite, Profissional, RedeSocial
        config_obj = ConfiguracaoSite.objects.filter(ativo=True).first()
        if config_obj:
            nome_instituto = config_obj.nome_instituto or nome_instituto
            conceito_triplice = config_obj.slogan_principal or conceito_triplice
            assinatura_institucional = config_obj.frase_institucional or assinatura_institucional
            assinatura_emocional = config_obj.frase_emocional or assinatura_emocional
            if config_obj.mensagem_whatsapp_padrao:
                mensagem_whatsapp = config_obj.mensagem_whatsapp_padrao
            if config_obj.whatsapp:
                whatsapp_numero = config_obj.whatsapp
                whatsapp_link = config_obj.whatsapp_link
            if config_obj.email:
                email_contato = config_obj.email
            if config_obj.instagram:
                instagram_url = config_obj.instagram

        profissional_destaque = Profissional.objects.filter(ativo=True, destaque=True).first()
        if profissional_destaque:
            nome_profissional = profissional_destaque.nome_exibicao or profissional_destaque.nome
            if profissional_destaque.registro_profissional:
                crp_profissional = profissional_destaque.registro_profissional

        redes_sociais = list(RedeSocial.objects.filter(ativo=True))
    except (OperationalError, ProgrammingError, Exception):
        # Em caso de banco não inicializado ou migrações pendentes, mantém os fallbacks
        config_obj = None

    # Fallback para whatsapp_link se ainda não gerado
    if not whatsapp_link and whatsapp_numero and whatsapp_numero != 'PENDENTE_DEFINICAO':
        numero_limpo = ''.join(filter(str.isdigit, str(whatsapp_numero)))
        if numero_limpo:
            msg_codificada = urllib.parse.quote(mensagem_whatsapp)
            whatsapp_link = f"https://wa.me/{numero_limpo}?text={msg_codificada}"

    return {
        'CONFIGURACAO_SITE': config_obj,
        'NOME_INSTITUTO': nome_instituto,
        'NOME_PROFISSIONAL': nome_profissional,
        'CONCEITO_TRIPLICE': conceito_triplice,
        'ASSINATURA_INSTITUCIONAL': assinatura_institucional,
        'ASSINATURA_EMOCIONAL': assinatura_emocional,
        'MENSAGEM_RODAPE': mensagem_rodape,
        'WHATSAPP_NUMERO': whatsapp_numero,
        'WHATSAPP_LINK': whatsapp_link,
        'WHATSAPP_MENSAGEM_PADRAO': mensagem_whatsapp,
        'EMAIL_CONTATO': email_contato,
        'INSTAGRAM_URL': instagram_url,
        'CRP_PROFISSIONAL': crp_profissional,
        'SITE_URL': site_url,
        'REDES_SOCIAIS': redes_sociais,
        'SEO_ALLOW_INDEXING': getattr(settings, 'SEO_ALLOW_INDEXING', False),
        'GOOGLE_SITE_VERIFICATION': getattr(settings, 'GOOGLE_SITE_VERIFICATION', ''),
        'BING_SITE_VERIFICATION': getattr(settings, 'BING_SITE_VERIFICATION', ''),
    }
