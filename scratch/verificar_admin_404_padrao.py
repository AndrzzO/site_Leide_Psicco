from django.test import Client, override_settings
c=Client(enforce_csrf_checks=True)
for debug in [True,False]:
    with override_settings(DEBUG=debug):
        for method in ['get','post']:
            for path in ['/admin/','/admin/login/','/admin/auth/user/']:
                r=getattr(c,method)(path)
                assert r.status_code==404
                assert b'site-header' not in r.content
                if not debug:
                    assert r.content==b'404 Not Found'
        print('404 verificado; DEBUG =',debug)
assert c.get('/area-cliente/entrar/').status_code==200
