"""
Templatetags para SEO Técnico e dados estruturados Schema.org (JSON-LD).
Inclui escape de segurança estrito anti-XSS e construtores de esquemas semânticos.
"""
import json
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


def get_site_url(custom_site_url=None):
    """Retorna a URL base do site normalizada sem barra final."""
    if custom_site_url:
        return str(custom_site_url).rstrip('/')
    return getattr(settings, 'SITE_URL', 'http://localhost:8000').rstrip('/')


@register.simple_tag
def build_absolute_url(path, site_url=None):
    """
    Gera uma URL absoluta a partir de um caminho relativo ou confirma uma URL já absoluta.
    """
    if not path:
        return get_site_url(site_url)
    str_path = str(path)
    if str_path.startswith('http://') or str_path.startswith('https://'):
        return str_path
    base = get_site_url(site_url)
    if not str_path.startswith('/'):
        str_path = '/' + str_path
    return f"{base}{str_path}"


@register.simple_tag
def render_json_ld(data, nonce=None):
    """
    Serializa um dicionário ou lista para JSON-LD com proteção estrita anti-XSS e compatibilidade CSP.
    Escapa sequências perigosas como '</script>' para '\\u003c/script\\u003e'
    impedindo encerramento prematuro da tag script e execução de código injetado.
    """
    if not data:
        return ''

    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # Substituição de segurança contra injeção de HTML/Scripts no contexto do navegador
    safe_json = (
        json_str.replace('</', r'<\u002F')
        .replace('<', r'\u003c')
        .replace('>', r'\u003e')
    )

    nonce_attr = f' nonce="{nonce}"' if nonce else ''
    return mark_safe(f'<script type="application/ld+json"{nonce_attr}>\n{safe_json}\n</script>')



@register.simple_tag(takes_context=True)
def render_global_schema(context):
    """
    Renderiza o grafo base institucional Schema.org (@graph):
    - WebSite (com SearchAction apontando para a busca interna)
    - Organization (Instituto Mente em Foco, com canais reais)
    - Person (Psicóloga Mari Menezes, fundada na realidade)
    """
    site_url = get_site_url(context.get('SITE_URL'))
    nome_instituto = context.get('NOME_INSTITUTO', 'Instituto Mente em Foco')
    conceito = context.get('CONCEITO_TRIPLICE', 'COMPREENDER • CUIDAR • RECONSTRUIR')
    assinatura = context.get('ASSINATURA_INSTITUCIONAL', '')
    nome_profissional = context.get('NOME_PROFISSIONAL', 'Psicóloga Mari Menezes')
    whatsapp = context.get('WHATSAPP_NUMERO', '')
    email = context.get('EMAIL_CONTATO', '')
    config_obj = context.get('CONFIGURACAO_SITE')

    # 1. Esquema WebSite
    website_schema = {
        "@type": "WebSite",
        "@id": f"{site_url}/#website",
        "url": f"{site_url}/",
        "name": nome_instituto,
        "description": f"{conceito} — {assinatura}",
        "publisher": {
            "@id": f"{site_url}/#organization"
        },
        "inLanguage": "pt-BR",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{site_url}/conteudos/?q={{search_term_string}}"
            },
            "query-input": "required name=search_term_string"
        }
    }

    # 2. Esquema Organization
    org_schema = {
        "@type": "Organization",
        "@id": f"{site_url}/#organization",
        "name": nome_instituto,
        "url": f"{site_url}/",
        "description": assinatura,
        "logo": f"{site_url}/static/img/identidade/logo_mente_em_foco.svg",
    }

    # Adiciona dados de contato apenas se factuais
    if whatsapp and whatsapp != 'PENDENTE_DEFINICAO':
        numero_limpo = ''.join(filter(str.isdigit, str(whatsapp)))
        if numero_limpo:
            org_schema["contactPoint"] = {
                "@type": "ContactPoint",
                "telephone": f"+{numero_limpo}",
                "contactType": "customer service",
                "availableLanguage": "Portuguese"
            }

    if email and email != 'PENDENTE_DEFINICAO':
        org_schema["email"] = email

    # Endereço factual se configurado no CMS
    if config_obj and getattr(config_obj, 'endereco_texto', None):
        address_dict = {
            "@type": "PostalAddress",
            "streetAddress": config_obj.endereco_texto,
        }
        if getattr(config_obj, 'cidade', None):
            address_dict["addressLocality"] = config_obj.cidade
        if getattr(config_obj, 'estado', None):
            address_dict["addressRegion"] = config_obj.estado
        if getattr(config_obj, 'cep', None):
            address_dict["postalCode"] = config_obj.cep
        address_dict["addressCountry"] = "BR"
        org_schema["address"] = address_dict

    # Redes sociais reais (apenas URLs válidas e definidas)
    redes = context.get('REDES_SOCIAIS', [])
    same_as = []
    for r in redes:
        r_url = getattr(r, 'url', None)
        if r_url and r_url != 'PENDENTE_DEFINICAO' and r_url.strip() and r_url.startswith(('http://', 'https://')):
            if r_url not in same_as:
                same_as.append(r_url)
    instagram = context.get('INSTAGRAM_URL', '')
    if instagram and instagram != 'PENDENTE_DEFINICAO' and instagram.startswith(('http://', 'https://')) and instagram not in same_as:
        same_as.append(instagram)
    if same_as:
        org_schema["sameAs"] = same_as

    # 3. Esquema Person (Mari Menezes)
    crp = context.get('CRP_PROFISSIONAL', '')
    person_schema = {
        "@type": "Person",
        "@id": f"{site_url}/#person-mari-menezes",
        "name": nome_profissional,
        "jobTitle": "Psicóloga Clínica e Neuropsicóloga",
        "url": f"{site_url}/sobre-mim/",
        "worksFor": {
            "@id": f"{site_url}/#organization"
        }
    }
    if crp and crp != 'PENDENTE_DEFINICAO':
        person_schema["identifier"] = crp

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            website_schema,
            org_schema,
            person_schema,
        ]
    }

    nonce = context.get('csp_nonce') if hasattr(context, 'get') else None
    return render_json_ld(graph, nonce=nonce)



@register.simple_tag(takes_context=True)
def render_breadcrumbs_schema(context, breadcrumbs_list):
    """
    Renderiza o esquema BreadcrumbList a partir de uma lista de dicionários
    [{'titulo': 'Nome', 'url': '/caminho/'}]
    """
    if not breadcrumbs_list:
        return ''

    site_url = get_site_url(context.get('SITE_URL'))
    items = []
    
    # Adiciona sempre a Home como posição 1 se não presente
    items.append({
        "@type": "ListItem",
        "position": 1,
        "name": "Início",
        "item": f"{site_url}/"
    })

    pos = 2
    for b in breadcrumbs_list:
        titulo = b.get('titulo') or b.get('name')
        url = b.get('url')
        if not titulo:
            continue
        if titulo.lower() in ['início', 'inicio', 'home']:
            continue

        item_dict = {
            "@type": "ListItem",
            "position": pos,
            "name": titulo,
        }
        if url:
            item_dict["item"] = build_absolute_url(url, site_url)
        items.append(item_dict)
        pos += 1

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

    nonce = context.get('csp_nonce') if hasattr(context, 'get') else None
    return render_json_ld(schema, nonce=nonce)


@register.simple_tag(takes_context=True)
def render_service_schema(context, servico=None, service_type="Psicoterapia / Avaliação"):
    """
    Renderiza o esquema Service para páginas de atendimento clínico e avaliativo.
    Garante ausência de notas/estrelas ou dados inventados, com suporte a fallbacks
    a partir do contexto caso o registro de banco ainda não esteja cadastrado.
    """
    site_url = get_site_url(context.get('SITE_URL'))
    nome = getattr(servico, 'nome', None) or getattr(servico, 'titulo', None) or context.get('titulo_pagina', 'Atendimento Especializado')
    if '|' in nome:
        nome = nome.split('|')[0].strip()
    if '—' in nome:
        nome = nome.split('—')[0].strip()

    resumo = getattr(servico, 'resumo', None) or getattr(servico, 'descricao', None) or context.get('meta_descricao', '')
    req = context.get('request')
    canonical_url = f"{site_url}{req.path}" if req else f"{site_url}/"

    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": nome,
        "description": resumo,
        "url": canonical_url,
        "serviceType": service_type,
        "provider": {
            "@id": f"{site_url}/#organization"
        },
        "areaServed": {
            "@type": "Country",
            "name": "Brasil"
        }
    }

    nonce = context.get('csp_nonce') if hasattr(context, 'get') else None
    return render_json_ld(schema, nonce=nonce)


@register.simple_tag(takes_context=True)
def render_article_schema(context, artigo):
    """
    Renderiza o esquema BlogPosting / Article para publicações do Blog.
    """
    if not artigo:
        return ''

    site_url = get_site_url(context.get('SITE_URL'))
    canonical_url = f"{site_url}{artigo.get_absolute_url()}"
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        },
        "headline": artigo.titulo,
        "description": artigo.resumo or artigo.meta_descricao,
        "url": canonical_url,
        "inLanguage": "pt-BR",
        "publisher": {
            "@id": f"{site_url}/#organization"
        },
        "author": {
            "@id": f"{site_url}/#person-mari-menezes"
        }
    }

    if artigo.data_publicacao:
        schema["datePublished"] = artigo.data_publicacao.isoformat()
    if artigo.data_atualizacao:
        schema["dateModified"] = artigo.data_atualizacao.isoformat()

    if artigo.imagem_capa:
        schema["image"] = f"{site_url}{artigo.imagem_capa.url}"

    nonce = context.get('csp_nonce') if hasattr(context, 'get') else None
    return render_json_ld(schema, nonce=nonce)

