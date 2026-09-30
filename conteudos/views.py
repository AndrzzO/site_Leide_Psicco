"""
Views do app conteudos (Blog / Conteúdos Educativos).
Gerencia listagem paginada, busca textual, filtragem por categoria temática,
destaque editorial, e visualização detalhada de artigos com sanitização estrita.
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from .models import CategoriaArtigo, Artigo


def index(request, categoria_slug=None):
    """
    Listagem pública de artigos educativos com busca, filtragem por categoria e paginação.
    Exibe apenas artigos com status 'publicado' e data_publicacao <= agora.
    """
    # Identifica categoria pela URL limpa ou por parâmetro GET
    slug_filtro = categoria_slug or request.GET.get('categoria', '').strip()
    categoria_selecionada = None
    if slug_filtro:
        categoria_selecionada = get_object_or_404(CategoriaArtigo, slug=slug_filtro, ativo=True)

    # Base de consulta: estritamente artigos publicados
    artigos_qs = Artigo.objects.publicados().select_related('categoria', 'autor')

    if categoria_selecionada:
        artigos_qs = artigos_qs.filter(categoria=categoria_selecionada)

    # Filtro de busca textual (com sanitização e limite de comprimento anti-DoS)
    query = request.GET.get('q', '').strip()
    if len(query) > 100:
        query = query[:100].strip()

    if query:
        artigos_qs = artigos_qs.filter(
            Q(titulo__icontains=query) |
            Q(resumo__icontains=query) |
            Q(conteudo__icontains=query)
        )

    # Página atual solicitada (com proteção contra valores inválidos ou excessivos)
    page_number = request.GET.get('page', 1)
    try:
        page_int = int(page_number)
        if page_int < 1:
            page_int = 1
        elif page_int > 10000:
            page_int = 10000
    except (ValueError, TypeError, OverflowError):
        page_int = 1

    # Destaque editorial: apenas na página inicial sem busca ou filtro específico, na primeira página
    artigo_destaque = None
    if not query and not categoria_selecionada and page_int == 1:
        artigo_destaque = artigos_qs.filter(destaque=True).first()
        if artigo_destaque:
            artigos_qs = artigos_qs.exclude(pk=artigo_destaque.pk)

    # Paginação: 9 artigos por página
    paginator = Paginator(artigos_qs, 9)
    try:
        artigos_paginados = paginator.page(page_int)
    except PageNotAnInteger:
        artigos_paginados = paginator.page(1)
    except EmptyPage:
        artigos_paginados = paginator.page(paginator.num_pages)

    # Categorias ativas para chips de navegação
    categorias = CategoriaArtigo.objects.filter(ativo=True).order_by('ordem', 'nome')

    # Definição de SEO
    meta_robots = None
    canonical_path = '/conteudos/'

    if categoria_selecionada:
        canonical_path = f'/conteudos/categoria/{categoria_selecionada.slug}/'
        meta_title = f"Artigos sobre {categoria_selecionada.nome} | Instituto Mente em Foco"
        meta_description = categoria_selecionada.descricao or (
            f"Confira artigos e orientações sobre {categoria_selecionada.nome} pelo Instituto Mente em Foco."
        )
    elif query:
        meta_robots = 'noindex, follow'
        canonical_path = '/conteudos/'
        meta_title = f"Busca por '{query}' | Conteúdos | Instituto Mente em Foco"
        meta_description = f"Resultados da busca editorial para '{query}' no Instituto Mente em Foco."
    else:
        meta_title = "Conteúdos, Artigos e Reflexões Clínicas | Instituto Mente em Foco"
        meta_description = (
            "Artigos educativos e reflexões sobre Psicologia Clínica, Relacionamentos, "
            "Traumas e Neuropsicologia pelo Instituto Mente em Foco."
        )

    contexto = {
        'artigos': artigos_paginados,
        'artigo_destaque': artigo_destaque,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
        'query': query,
        'total_resultados': paginator.count + (1 if artigo_destaque else 0),
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_robots': meta_robots,
        'canonical_path': canonical_path,
    }
    return render(request, 'conteudos/index.html', contexto)


def detalhe(request, slug):
    """
    Visualização detalhada de um artigo educativo individual.
    Garante acesso exclusivo a artigos devidamente publicados.
    Rascunhos e agendamentos futuros geram 404 para o público geral.
    """
    artigo = get_object_or_404(
        Artigo.objects.publicados().select_related('categoria', 'autor', 'servico_relacionado'),
        slug=slug
    )

    # Artigos relacionados: prioriza mesma categoria, complementa com outros publicados
    relacionados = list(
        Artigo.objects.publicados()
        .filter(categoria=artigo.categoria)
        .exclude(pk=artigo.pk)
        .select_related('categoria')[:3]
    )
    if len(relacionados) < 3:
        ids_excluidos = [artigo.pk] + [r.pk for r in relacionados]
        complementares = list(
            Artigo.objects.publicados()
            .exclude(pk__in=ids_excluidos)
            .select_related('categoria')[:3 - len(relacionados)]
        )
        relacionados.extend(complementares)

    # SEO dinâmico por artigo
    meta_title = artigo.meta_titulo or f"{artigo.titulo} | Instituto Mente em Foco"
    if artigo.meta_descricao:
        meta_description = artigo.meta_descricao
    elif artigo.resumo:
        meta_description = artigo.resumo
    else:
        conteudo_limpo = strip_tags(artigo.conteudo_formatado)
        meta_description = conteudo_limpo[:155] + ('...' if len(conteudo_limpo) > 155 else '')

    og_image = artigo.imagem_capa.url if artigo.imagem_capa else None

    # Estrutura de breadcrumb para navegação e Schema BreadcrumbList
    breadcrumb = [
        {'titulo': 'Conteúdos', 'url': '/conteudos/'},
    ]
    if artigo.categoria:
        breadcrumb.append({
            'titulo': artigo.categoria.nome,
            'url': f'/conteudos/categoria/{artigo.categoria.slug}/'
        })
    breadcrumb.append({'titulo': artigo.titulo, 'url': None})

    contexto = {
        'artigo': artigo,
        'artigos_relacionados': relacionados,
        'servico_relacionado': artigo.servico_relacionado,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'og_image': og_image,
        'breadcrumb': breadcrumb,
    }
    return render(request, 'conteudos/detalhe.html', contexto)
