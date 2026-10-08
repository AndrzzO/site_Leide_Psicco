from pathlib import Path
p=Path('configuracoes/urls.py');s=p.read_text(encoding='utf-8-sig').replace('from django.urls import path, include','from django.urls import path, include, re_path\nimport re');s=s.replace('from nucleo.views import robots_txt','from nucleo.views import robots_txt, admin_indisponivel');s=s.replace('    path(admin_path, admin.site.urls),', "    re_path(r'^' + re.escape(admin_path.rstrip('/')) + r'(?:/.*)?$', admin_indisponivel),\n    re_path(r'^admin(?:/.*)?$', admin_indisponivel),");p.write_text(s,encoding='utf-8')
p=Path('nucleo/views.py');s=p.read_text(encoding='utf-8-sig');s+='''

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def admin_indisponivel(request):
    """Endpoint desativado: nenhum método executa ações administrativas."""
    response = tratar_erro_404(request)
    response['Cache-Control'] = 'no-store, private'
    response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    return response
''';p.write_text(s,encoding='utf-8')
