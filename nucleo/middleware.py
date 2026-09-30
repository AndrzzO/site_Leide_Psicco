from django.conf import settings


class SecurityHeadersMiddleware:
    """
    Middleware defensivo para injeção de cabeçalhos de segurança HTTP modernos:
    - Permissions-Policy: restringe acesso a APIs do navegador não utilizadas (câmera, microfone, geolocalização, usb, etc.)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault(
            'Permissions-Policy',
            'camera=(), microphone=(), geolocation=(), payment=(), usb=()'
        )
        return response



class SEOMiddleware:
    """
    Middleware de governança de indexação de busca via cabeçalho HTTP X-Robots-Tag.
    Garante que:
    1. Ambientes de homologação, staging e desenvolvimento NUNCA sejam indexados por engano.
    2. Em produção, páginas de erro (4xx, 5xx), health check, design system,
       pesquisa interna (?q=...) e páginas legais tenham diretivas restritivas apropriadas.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        allow_indexing = getattr(settings, 'SEO_ALLOW_INDEXING', False)

        # Regra 1: Bloqueio absoluto se o ambiente não tiver indexação autorizada
        if not allow_indexing:
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            return response

        # Regra 2: Se a view já definiu explicitamente o cabeçalho, preserva
        if 'X-Robots-Tag' in response:
            return response

        # Regra 3: Tratamento de status de erro (4xx ou 5xx)
        if response.status_code >= 400:
            response['X-Robots-Tag'] = 'noindex, nofollow'
            return response

        path = request.path

        # Regra 4: Rotas técnicas internas e de utilidade
        if path.startswith('/health/') or path.startswith('/design-system/'):
            response['X-Robots-Tag'] = 'noindex, nofollow'
            return response

        # Regra 5: Resultados de pesquisa interna (/conteudos/?q=...)
        if request.GET.get('q'):
            response['X-Robots-Tag'] = 'noindex, follow'
            return response

        # Regra 6: Rotas de políticas e termos (devem ser seguidas, mas priorizadas como canônicas / noindex)
        if path in ['/politica-de-privacidade/', '/politica-de-cookies/', '/privacidade/', '/cookies/']:
            response['X-Robots-Tag'] = 'noindex, follow'
            return response

        return response
