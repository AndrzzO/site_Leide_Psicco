from django.conf import settings
from django.test import Client
client = Client(enforce_csrf_checks=True)
base = '/' + settings.DJANGO_ADMIN_URL.strip('/')
for url in set(['/admin', '/admin/', '/admin/login/', '/admin/auth/user/', base, base+'/',base+'/login/',base+'/auth/user/']):
    for method in ['get','post']:
        response=getattr(client,method)(url)
        assert response.status_code==404, (url, method, response.status_code)
        assert b'<!DOCTYPE html>' in response.content or b'<!doctype html>' in response.content.lower()
print('Admin: GET e POST retornam 404 em todas as rotas verificadas.')
assert client.get('/area-cliente/entrar/').status_code==200
print('Login do Blog permanece disponível.')
