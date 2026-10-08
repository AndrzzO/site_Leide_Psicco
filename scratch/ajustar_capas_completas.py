from pathlib import Path
p=Path('static/css/conteudos.css');s=p.read_text(encoding='utf-8-sig')
for selector in ['.card-destaque-editorial__capa', '.card-artigo-item__capa', '.artigo-capa-wrap img']:
 start=s.index(selector+' {');end=s.index('}',start)
 block=s[start:end].replace('object-fit: cover;', 'object-fit: contain;\n  background-color: var(--cor-areia-clara, #f0e9dd);')
 if selector=='.card-destaque-editorial__capa':
  block=block.replace('  width: 100%;','  position: absolute;\n  inset: 0;\n  width: 100%;')
 s=s[:start]+block+s[end:]
s=s.replace('transform: scale(1.03);','transform: none;').replace('transform: scale(1.04);','transform: none;')
p.write_text(s,encoding='utf-8')
