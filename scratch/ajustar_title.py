from pathlib import Path
p=Path('servicos/views.py')
s=p.read_text(encoding='utf-8').replace("'titulo_pagina': 'Avaliações, Laudos e Pareceres | Instituto Mente em Foco'", "'titulo_pagina': 'Avaliações Psicológicas e Documentos | Instituto Mente em Foco'")
p.write_text(s,encoding='utf-8')

