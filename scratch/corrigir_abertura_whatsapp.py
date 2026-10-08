from pathlib import Path
p=Path('contato/views.py');s=p.read_text(encoding='utf-8-sig').replace("if request.POST.get('destino') == 'whatsapp':", "if request.POST.get('destino', 'whatsapp') == 'whatsapp':");s=s.replace('resposta = redirect(f"https://wa.me/{numero}?text={quote(texto, safe=\'\')}")', '''resposta = render(request, 'contato/abrir_whatsapp.html', {
                        'whatsapp_destino': f"https://wa.me/{numero}?text={quote(texto, safe='')}",
                        'texto_whatsapp': texto,
                    })''');p.write_text(s,encoding='utf-8')
p=Path('contato/tests_whatsapp.py');s=p.read_text(encoding='utf-8-sig').replace('self.assertEqual(response.status_code, 302)','self.assertEqual(response.status_code, 200)').replace('url = urlsplit(response.url)', "url = urlsplit(response.context['whatsapp_destino'])");p.write_text(s,encoding='utf-8')
