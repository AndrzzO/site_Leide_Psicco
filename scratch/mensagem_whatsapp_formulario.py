from pathlib import Path
p=Path('contato/views.py');s=p.read_text(encoding='utf-8-sig').replace('import logging','import logging\nfrom urllib.parse import quote, urlsplit');marker='            # Salva mensagem legítima no banco';s=s.replace(marker,'''            if request.POST.get('destino') == 'whatsapp':
                from nucleo.context_processors import dados_institucionais
                link_padrao = dados_institucionais(request)['WHATSAPP_LINK']
                if link_padrao:
                    dados = form.cleaned_data
                    linhas = [f"Olá Dra. Marileide, me chamo {dados['nome']}."]
                    servico = dados.get('servico_interesse')
                    linhas.append(f"Quero saber mais a respeito de {servico.nome}." if servico else 'Quero saber mais a respeito dos seus atendimentos.')
                    if dados.get('mensagem'):
                        linhas.append(dados['mensagem'])
                    contatos = []
                    if dados.get('telefone'):
                        contatos.append(f"Telefone: {dados['telefone']}")
                    if dados.get('email'):
                        contatos.append(f"E-mail: {dados['email']}")
                    linhas.append('\\n'.join(contatos))
                    numero = urlsplit(link_padrao).path.strip('/')
                    resposta = redirect(f"https://wa.me/{numero}?text={quote(chr(10).join([linha + chr(10) for linha in linhas]).strip(), safe='')}")
                    resposta['Cache-Control'] = 'no-store, private'
                    resposta['Referrer-Policy'] = 'no-referrer'
                    return resposta

'''+marker);s=s.replace("        'form': form,", "        'form': form,\n        'enviar_whatsapp': True,");p.write_text(s,encoding='utf-8')
p=Path('templates/componentes/formulario_contato.html');s=p.read_text(encoding='utf-8-sig').replace('{% csrf_token %}',"{% csrf_token %}\n                    {% if enviar_whatsapp and WHATSAPP_LINK %}<input type=\"hidden\" name=\"destino\" value=\"whatsapp\">{% endif %}");s=s.replace("{{ botao_texto|default:'Enviar mensagem' }}", "{% if enviar_whatsapp and WHATSAPP_LINK %}Continuar no WhatsApp{% else %}{{ botao_texto|default:'Enviar mensagem' }}{% endif %}");s=s.replace('                </form>', '                    {% if enviar_whatsapp and WHATSAPP_LINK %}<p class="form-label__dica">Seus dados serão incluídos na mensagem. Confira no WhatsApp e toque em Enviar para concluir.</p>{% endif %}\n                </form>');p.write_text(s,encoding='utf-8')
