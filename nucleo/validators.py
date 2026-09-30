"""
Validadores de segurança para arquivos e imagens enviados no Django Admin.
Protege contra arquivos executáveis, arquivos excessivamente grandes e formatos maliciosos.
"""
import os
from django.core.exceptions import ValidationError
from PIL import Image

# Limites e extensões permitidas para uploads de imagem
TAMANHO_MAXIMO_IMAGEM_MB = 10
TAMANHO_MAXIMO_IMAGEM_BYTES = TAMANHO_MAXIMO_IMAGEM_MB * 1024 * 1024
EXTENSOES_PERMITIDAS = {'.jpg', '.jpeg', '.png', '.webp', '.ico'}
FORMATOS_PIL_PERMITIDOS = {'JPEG', 'PNG', 'WEBP', 'ICO'}


def validar_tamanho_imagem(arquivo):
    """Verifica se o arquivo respeita o limite máximo de tamanho."""
    if arquivo.size > TAMANHO_MAXIMO_IMAGEM_BYTES:
        raise ValidationError(
            f'O arquivo excede o limite máximo permitido de {TAMANHO_MAXIMO_IMAGEM_MB} MB. '
            f'Tamanho atual: {arquivo.size / (1024 * 1024):.1f} MB.'
        )


def validar_formato_imagem(arquivo):
    """
    Valida a extensão e a integridade da imagem utilizando Pillow.
    Garante que arquivos maliciosos ou renomeados com extensões falsas sejam rejeitados.
    """
    ext = os.path.splitext(arquivo.name)[1].lower()
    if ext not in EXTENSOES_PERMITIDAS:
        extensoes_formatadas = ', '.join(sorted(EXTENSOES_PERMITIDAS))
        raise ValidationError(
            f'Extensão de arquivo "{ext}" não permitida. '
            f'Formatos aceitos: {extensoes_formatadas}.'
        )

    # Verifica integridade real do cabeçalho da imagem via Pillow
    try:
        arquivo.seek(0)
        imagem = Image.open(arquivo)
        imagem.verify()
        formato = imagem.format.upper()
        if formato not in FORMATOS_PIL_PERMITIDOS:
            raise ValidationError(
                f'Formato interno de imagem "{formato}" não é suportado. '
                f'Formatos aceitos: JPG, PNG, WEBP, ICO.'
            )
        arquivo.seek(0)
    except Exception as exc:
        arquivo.seek(0)
        if isinstance(exc, ValidationError):
            raise exc
        raise ValidationError('O arquivo enviado não é uma imagem válida ou está corrompido.')


def validar_imagem(arquivo):
    """Validador composto para tamanho e formato de imagem."""
    validar_tamanho_imagem(arquivo)
    validar_formato_imagem(arquivo)
