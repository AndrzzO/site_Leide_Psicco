from functools import wraps
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from nucleo.login_security import proteger_login
from nucleo.models import Profissional
from .models import Artigo
from .painel_forms import LoginProprietariaForm, ArtigoEditorForm


def privada(view):
    @wraps(view)
    @never_cache
    def resposta(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        result['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return result
    return resposta


def editora(view):
    return privada(login_required(permission_required('conteudos.gerenciar_blog', raise_exception=True)(view), login_url='painel:login'))


@proteger_login
def entrar(request):
    if request.method == 'GET' and request.user.has_perm('conteudos.gerenciar_blog'):
        return redirect('painel:index')
    form = LoginProprietariaForm(request, data=request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        request.session.set_expiry(3600 * 4)
        return redirect('painel:index')
    return render(request, 'conteudos/painel/login.html', {'form': form})


@editora
def index(request):
    artigos = Artigo.objects.select_related('categoria').order_by('-data_atualizacao')
    return render(request, 'conteudos/painel/index.html', {'page_obj': Paginator(artigos, 20).get_page(request.GET.get('page'))})


@editora
def editar(request, pk=None):
    artigo = get_object_or_404(Artigo, pk=pk) if pk else Artigo()
    form = ArtigoEditorForm(request.POST or None, request.FILES or None, instance=artigo)
    if request.method == 'POST' and form.is_valid():
        artigo = form.save(commit=False)
        artigo.formato_html = True
        artigo.status = Artigo.STATUS_PUBLICADO if request.POST.get('acao') == 'publicar' else Artigo.STATUS_RASCUNHO
        if not artigo.autor_id:
            artigo.autor = Profissional.objects.filter(ativo=True).first()
        artigo.save()
        messages.success(request, 'Artigo publicado.' if artigo.status == Artigo.STATUS_PUBLICADO else 'Rascunho salvo.')
        return redirect('painel:index')
    return render(request, 'conteudos/painel/editor.html', {'form': form, 'artigo': artigo})


@editora
def excluir(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        artigo.delete()
        messages.success(request, 'Artigo excluído.')
        return redirect('painel:index')
    return render(request, 'conteudos/painel/excluir.html', {'artigo': artigo})


@privada
@require_POST
def sair(request):
    logout(request)
    return redirect('painel:login')
