from pathlib import Path
from PIL import Image, ImageOps
import shutil
source=Path(r'C:\Users\andre\.codex\generated_images\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\exec-0ba1914f-5bd1-49d8-9642-0a4fba0d1b7a.png')
shutil.copy2(source,'scratch/imagens_reformulacao_originais/bariatrica-v2.png')
im=Image.open(source).convert('RGB')
for name,size in [('bariatrica-v2.webp',(960,640)),('bariatrica-v2-mobile.webp',(640,480))]:
    ImageOps.fit(im,size,method=Image.Resampling.LANCZOS).save(Path('static/img/avaliacoes')/name,'WEBP',quality=84,method=6)
p=Path('servicos/editorial.py')
s=p.read_text(encoding='utf-8-sig').replace('"imagem": "bariatrica",','"imagem": "bariatrica-v2",').replace('Mulher sentada à mesa com um caderno fechado, olhando para o jardim.','Duas mulheres conversam em poltronas; uma delas apoia a mão sobre a mão da outra.')
p.write_text(s,encoding='utf-8')
p=Path('scratch/verificar_burnout_v2.cjs')
s=p.read_text(encoding='utf-8-sig').replace('burnout-v2','bariatrica-v2').replace('/avaliacao/burnout/','/avaliacao/cirurgia-bariatrica/')
Path('scratch/verificar_bariatrica_v2.cjs').write_text(s,encoding='utf-8')

