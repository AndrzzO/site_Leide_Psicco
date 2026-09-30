"""
Funções seguras para definição de caminhos de upload de arquivos e imagens.
Previne Directory Traversal, padroniza extensões e organiza mídias por contexto.
"""
import os
import uuid
from django.utils.text import slugify


def _gerar_caminho_seguro(subpasta, nome_base, arquivo_nome):
    """Gera um caminho seguro dentro da subpasta especificada."""
    ext = os.path.splitext(arquivo_nome)[1].lower()
    identificador = uuid.uuid4().hex[:8]
    slug_limpo = slugify(nome_base)[:40] if nome_base else 'imagem'
    novo_nome = f"{slug_limpo}_{identificador}{ext}"
    return os.path.join(subpasta, novo_nome)


def caminho_upload_institucional(instance, filename):
    """Caminho para logotipos, favicon e Open Graph."""
    return _gerar_caminho_seguro('institucional', 'marca', filename)


def caminho_upload_profissional(instance, filename):
    """Caminho para fotos da profissional Mari Menezes."""
    nome_base = getattr(instance, 'slug', 'profissional')
    return _gerar_caminho_seguro('profissionais', nome_base, filename)


def caminho_upload_area(instance, filename):
    """Caminho para imagens dos cards de áreas de atuação."""
    nome_base = getattr(instance, 'slug', 'area')
    return _gerar_caminho_seguro('areas', nome_base, filename)


def caminho_upload_servico(instance, filename):
    """Caminho para imagens de serviços e avaliações."""
    nome_base = getattr(instance, 'slug', 'servico')
    return _gerar_caminho_seguro('servicos', nome_base, filename)


def caminho_upload_artigo(instance, filename):
    """Caminho para imagens de capa de artigos do blog."""
    nome_base = getattr(instance, 'slug', 'artigo')
    return _gerar_caminho_seguro('artigos', nome_base, filename)
