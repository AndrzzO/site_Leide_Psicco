"""
Módulo de Sanitização e Renderização Segura de Conteúdo Editorial.
Garante conversão de Markdown controlado e sanitização estrita via Bleach,
impedindo injeção de scripts (XSS), tags perigosas e atributos maliciosos.
"""
import markdown
import bleach


# Allowlist rigorosa de elementos HTML estruturais permitidos
ALLOWED_TAGS = [
    'h2', 'h3', 'h4', 'p', 'br', 'strong', 'em', 'ul', 'ol', 'li',
    'blockquote', 'a', 'hr', 'code', 'pre'
]

# Atributos estritamente permitidos por tag
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel', 'target'],
}

# Protocolos de URL permitidos
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def renderizar_markdown_seguro(conteudo_md: str) -> str:
    """
    Converte texto Markdown para HTML e aplica sanitização estrita via Bleach.
    Bloqueia scripts, iframes, estilos inline, atributos como onerror/onclick,
    e tags <h1> para preservar a hierarquia de título único na página.
    """
    if not conteudo_md:
        return ''

    # 1. Conversão de Markdown para HTML
    html_bruto = markdown.markdown(
        conteudo_md,
        extensions=['extra', 'nl2br'],
        output_format='html5'
    )

    # 2. Sanitização com Bleach via allowlist
    html_sanitizado = bleach.clean(
        html_bruto,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )

    return html_sanitizado.strip()
