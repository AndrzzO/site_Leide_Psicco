from pathlib import Path
from PIL import Image, ImageOps
import json, shutil
mapping=json.loads(r'''{"burnout":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-4d33da1c-ecd5-4a3e-81ce-21a05b7b274b.png","bariatrica":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-85ca521f-41ba-4c2a-8ef2-866ab933f8d7.png","esterilizacao":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-84d9967a-4270-401d-bc15-fc34672de472.png","inss":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-33e32d07-8820-498d-979a-97d36accc68c.png","judicial":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-cb51ff3b-004b-45c0-8f06-8f6079575835.png","ansiedade":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-11195fa9-a052-40f7-8e7c-ae3c30e126e5.png","psicoterapia":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-6c131f6f-f637-4cd5-8b7c-902b2f244450.png","credenciamento":"C:\\Users\\andre\\.codex\\generated_images\\01a0ebd3-dccd-76f2-a0ea-1f8c9958dd5f\\exec-530222d9-23a4-4305-bd7d-be0eefbc3f25.png"}''')
dest=Path('static/img/avaliacoes'); dest.mkdir(parents=True,exist_ok=True)
originals=Path('scratch/imagens_reformulacao_originais'); originals.mkdir(exist_ok=True)
for name, source in mapping.items():
    shutil.copy2(source, originals/(name+'.png'))
    im=Image.open(source).convert('RGB')
    ImageOps.fit(im,(960,640),method=Image.Resampling.LANCZOS).save(dest/(name+'.webp'),'WEBP',quality=82,method=6)
    ImageOps.fit(im,(640,480),method=Image.Resampling.LANCZOS,centering=(.5,.5)).save(dest/(name+'-mobile.webp'),'WEBP',quality=80,method=6)
    print(name, (dest/(name+'.webp')).stat().st_size, (dest/(name+'-mobile.webp')).stat().st_size)

