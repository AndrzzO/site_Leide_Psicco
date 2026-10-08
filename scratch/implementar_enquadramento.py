from pathlib import Path
p=Path('conteudos/models.py');s=p.read_text(encoding='utf-8-sig').replace('from django.db import models','from django.db import models\nfrom django.core.validators import MinValueValidator, MaxValueValidator');s=s.replace('    fonte = models.CharField',"    capa_x = models.PositiveSmallIntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])\n    capa_y = models.PositiveSmallIntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])\n    fonte = models.CharField");p.write_text(s,encoding='utf-8')
p=Path('conteudos/painel_forms.py');s=p.read_text(encoding='utf-8-sig').replace("    permanencia =", "    capa_x = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.HiddenInput())\n    capa_y = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.HiddenInput())\n    permanencia =");s=s.replace("'imagem_capa', 'texto_alternativo_imagem'", "'imagem_capa', 'capa_x', 'capa_y', 'texto_alternativo_imagem'");s=s.replace('        dados = super().clean()', "        dados = super().clean()\n        for eixo in ('capa_x', 'capa_y'):\n            if eixo not in self.errors and dados.get(eixo) is None:\n                dados[eixo] = getattr(self.instance, eixo, 50)");p.write_text(s,encoding='utf-8')
p=Path('templates/conteudos/painel/editor.html');s=p.read_text(encoding='utf-8-sig');s=s.replace('<div class="painel-campo">{{ form.texto_alternativo_imagem.label_tag }}', '''{{ form.capa_x }}{{ form.capa_y }}{{ form.capa_x.errors }}{{ form.capa_y.errors }}
<div id="capa-ajuste" hidden>
<p class="capa-instrucao" id="capa-instrucao">Arraste a foto para escolher o enquadramento.</p>
<div id="capa-quadro" tabindex="0" role="group" aria-label="Enquadramento da capa" aria-describedby="capa-instrucao"><img id="capa-previa" {% if artigo.imagem_capa %}src="{{ artigo.imagem_capa.url }}"{% endif %} alt="Prévia do enquadramento da capa" draggable="false"></div>
<button type="button" id="capa-centralizar" class="painel-link">Centralizar foto</button>
<small id="capa-aviso" role="status">Você também pode usar as setas do teclado. O enquadramento será salvo junto com o artigo.</small>
</div>
<div class="painel-campo">{{ form.texto_alternativo_imagem.label_tag }}''');s=s.replace("<script src=\"{% static 'js/editor-blog.js' %}\" defer></script>","<script src=\"{% static 'js/editor-blog.js' %}\" defer></script><script src=\"{% static 'js/enquadramento-capa.js' %}\" defer></script>");p.write_text(s,encoding='utf-8')
for file in ['templates/conteudos/index.html','templates/conteudos/detalhe.html']:
 p=Path(file);s=p.read_text(encoding='utf-8-sig')
 for nome in ['artigo','artigo_destaque','rel']:
  src='src="{{ '+nome+'.imagem_capa.url }}"'
  s=s.replace(src,src+' style="object-position: {{ '+nome+'.capa_x }}% {{ '+nome+'.capa_y }}%;"')
 p.write_text(s,encoding='utf-8')
