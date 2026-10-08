from pathlib import Path
from PIL import Image, ImageOps
import shutil
source=Path(r'C:\Users\andre\.codex\generated_images\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\exec-6e3d5733-92e9-453c-bbd9-8fd7e9b1ebbb.png')
dest=Path('static/img/avaliacoes')
shutil.copy2(source,Path('scratch/imagens_reformulacao_originais/burnout-v2.png'))
im=Image.open(source).convert('RGB')
for name,size in [('burnout-v2.webp',(960,640)),('burnout-v2-mobile.webp',(640,480))]:
    ImageOps.fit(im,size,method=Image.Resampling.LANCZOS).save(dest/name,'WEBP',quality=84,method=6)
p=Path('servicos/editorial.py')
s=p.read_text(encoding='utf-8-sig').replace('"imagem": "burnout",','"imagem": "burnout-v2",').replace('Mulher junto à janela, com um computador fechado sobre a mesa.','Homem com as mãos nas têmporas diante de um notebook, cercado por pessoas com pastas, papéis e um celular.')
p.write_text(s,encoding='utf-8')
print('Imagem de burnout atualizada nas versões desktop e mobile.')

