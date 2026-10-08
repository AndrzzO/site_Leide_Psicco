from pathlib import Path
from PIL import Image
import os,json,shutil
os.environ.setdefault('DJANGO_SETTINGS_MODULE','configuracoes.settings.desenvolvimento')
import django
django.setup()
from nucleo.models import Profissional
root=Path.cwd()
source=Path(r'C:/Users/andre/Downloads/WhatsApp Image 2026-09-26 at 11.52.39 (3).jpeg')
im=Image.open(source)
print('Montagem:',im.size)
dest=root/'media/profissionais'
dest.mkdir(exist_ok=True,parents=True)
# Extração dos painéis existentes, sem síntese ou retoque.
regions={'mari-capa-v3.webp':(0,0,760,1024),'mari-mesa-v3.webp':(774,0,1536,532),'mari-escrevendo-v3.webp':(1162,545,1536,1024)}
for name,box in regions.items():
    im.crop(box).save(dest/name,'WEBP',quality=92,method=6)
prof=Profissional.objects.filter(ativo=True).first()
assert prof is not None, 'Cadastro profissional ativo não encontrado.'
backup=root/'scratch/fotos_mari_antes_v3.json'
if not backup.exists():
    backup.write_text(json.dumps({'pk':prof.pk,'foto_principal':prof.foto_principal.name,'foto_sobre':prof.foto_sobre.name,'foto_secundaria':prof.foto_secundaria.name},ensure_ascii=False,indent=2),encoding='utf-8')
prof.foto_principal='profissionais/mari-capa-v3.webp'
prof.foto_sobre='profissionais/mari-mesa-v3.webp'
prof.foto_secundaria='profissionais/mari-escrevendo-v3.webp'
prof.save(update_fields=['foto_principal','foto_sobre','foto_secundaria'])
def edit(path,old,new):
    p=root/path;s=p.read_text(encoding='utf-8-sig');assert old in s,path;s=s.replace(old,new);p.write_text(s,encoding='utf-8')
edit('templates/paginas/home.html','alt="Mari Menezes, de óculos e blazer claro, sorrindo." width="819" height="1024"','alt="Mari Menezes sorrindo e olhando para a câmera." width="760" height="1024"')
edit('templates/paginas/home.html','<figure class="editorial-foto"><img src="{% static \'img/avaliacoes/psicoterapia.webp\' %}" alt="Duas poltronas de linho voltadas uma para a outra junto à janela." width="960" height="640" loading="lazy"><figcaption>Imagem temática ilustrativa.</figcaption></figure>','{% if profissional.foto_secundaria %}<figure class="editorial-foto editorial-foto--mari-escrevendo"><img src="{{ profissional.foto_secundaria.url }}" alt="Mari Menezes sorrindo enquanto escreve em um caderno." width="374" height="479" loading="lazy" decoding="async"><figcaption>Mari Menezes · Escuta e cuidado.</figcaption></figure>{% else %}<figure class="editorial-foto"><img src="{% static \'img/avaliacoes/psicoterapia.webp\' %}" alt="Duas poltronas de linho voltadas uma para a outra junto à janela." width="960" height="640" loading="lazy"></figure>{% endif %}')
edit('templates/paginas/sobre_mim.html','imagem_ratio="ratio-4-5"','imagem_ratio="ratio-4-3"')
edit('templates/paginas/sobre_mim.html','imagem_alt="Psicóloga Mari Menezes — Instituto Mente em Foco"','imagem_alt="Mari Menezes sorrindo, sentada à mesa com um caderno."')
edit('templates/paginas/sobre_mim.html','<div class="media-frame ratio-4-3 split-editorial__frame">','<div class="media-frame ratio-4-5 split-editorial__frame retrato-mari-escrevendo">')
edit('templates/paginas/sobre_mim.html','alt="Consultório e ambiente de acolhimento do Instituto Mente em Foco"','alt="Mari Menezes sorrindo enquanto escreve em um caderno." width="374" height="479"')
with (root/'static/css/editorial.css').open('a',encoding='utf-8') as f:
    f.write('\n/* Fotografias reais extraídas da montagem aprovada em 30/09/2026. */\n.editorial-retrato img{object-position:center 18%}\n.editorial-foto--mari-escrevendo{max-width:374px;width:100%;justify-self:center}\n.editorial-foto--mari-escrevendo img{aspect-ratio:374/479;object-fit:contain}\n.retrato-mari-escrevendo{max-width:374px;margin-inline:auto}\n')
print('Três fotografias atualizadas nos campos existentes do CMS.')

