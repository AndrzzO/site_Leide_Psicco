from pathlib import Path
from PIL import Image, ImageOps
import shutil
source=Path(r'C:\Users\andre\.codex\generated_images\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\exec-03e5b2bd-f146-4bc8-bcf6-2d2f9e4f5272.png')
shutil.copy2(source,'scratch/imagens_reformulacao_originais/ansiedade-v2.png')
im=Image.open(source).convert('RGB')
for name,size in [('ansiedade-v2.webp',(960,640)),('ansiedade-v2-mobile.webp',(640,480))]:
    ImageOps.fit(im,size,method=Image.Resampling.LANCZOS).save(Path('static/img/avaliacoes')/name,'WEBP',quality=84,method=6)
p=Path('servicos/editorial.py')
s=p.read_text(encoding='utf-8-sig').replace('"imagem": "ansiedade",','"imagem": "ansiedade-v2",').replace('Homem sentado em um sofá de linho junto a uma janela iluminada.','Mulher e homem de pele escura com as mãos na cabeça, diante de linhas emaranhadas que representam pensamentos em excesso.')
p.write_text(s,encoding='utf-8')
p=Path('scratch/verificar_burnout_v2.cjs')
s=p.read_text(encoding='utf-8-sig').replace('burnout-v2','ansiedade-v2').replace('/avaliacao/burnout/','/avaliacao/ansiedade-depressao/')
Path('scratch/verificar_ansiedade_v2.cjs').write_text(s,encoding='utf-8')

