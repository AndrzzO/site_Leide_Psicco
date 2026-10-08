from pathlib import Path
from PIL import Image, ImageOps
import shutil
source=Path(r'C:\Users\andre\.codex\generated_images\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\exec-13b0f1f8-fd8d-4b70-b52c-f9470286c468.png')
shutil.copy2(source,'scratch/imagens_reformulacao_originais/esterilizacao-v2.png')
im=Image.open(source).convert('RGB')
for name,size in [('esterilizacao-v2.webp',(960,640)),('esterilizacao-v2-mobile.webp',(640,480))]:
    ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(.5,0)).save(Path('static/img/avaliacoes')/name,'WEBP',quality=84,method=6)
p=Path('servicos/editorial.py')
s=p.read_text(encoding='utf-8-sig').replace('"imagem": "esterilizacao",','"imagem": "esterilizacao-v2",').replace('Pessoa com um caderno no colo, sentada em uma varanda iluminada.','Homem e mulher lado a lado, de frente, cada um segurando uma corda com nó na altura da pelve.')
p.write_text(s,encoding='utf-8')
p=Path('static/css/editorial.css')
with p.open('a',encoding='utf-8') as f: f.write('\n/* Preserva rostos e cordas nos recortes da imagem de esterilização. */\nimg[src*="esterilizacao-v2"]{object-position:center top}\n')
p=Path('scratch/verificar_burnout_v2.cjs')
s=p.read_text(encoding='utf-8-sig').replace('burnout-v2','esterilizacao-v2').replace('/avaliacao/burnout/','/avaliacao/esterilizacao/')
Path('scratch/verificar_esterilizacao_v2.cjs').write_text(s,encoding='utf-8')

