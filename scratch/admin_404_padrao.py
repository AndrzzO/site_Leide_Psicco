from pathlib import Path
p=Path('nucleo/views.py');s=p.read_text(encoding='utf-8-sig');s=s.replace('    return render(request, \'erros/404.html\', status=404)', '''    if getattr(request, '_admin_desativado', False):
        from django.http import HttpResponseNotFound
        response = HttpResponseNotFound('404 Not Found', content_type='text/plain; charset=utf-8')
        response['Cache-Control'] = 'no-store, private'
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
    return render(request, 'erros/404.html', status=404)''');s=s.replace('''    response = tratar_erro_404(request)
    response['Cache-Control'] = 'no-store, private'
    response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    return response''','''    from django.http import Http404
    request._admin_desativado = True
    raise Http404('Página não encontrada.')''');p.write_text(s,encoding='utf-8')
