from pathlib import Path
for p in ['static/css/componentes.css','static/js/navegacao.js']:
    path=Path(p); s=path.read_text(encoding='utf-8-sig').replace('min-width: 1080px','min-width: 1200px').replace('Breakpoint Desktop 1080px','Breakpoint Desktop 1200px'); path.write_text(s,encoding='utf-8')
p=Path('static/css/editorial.css')
with p.open('a',encoding='utf-8') as f:
    f.write("""
.editorial-final p{color:#f7f3eb}
.editorial-breadcrumb a{color:#46553e;text-underline-offset:3px}
.site-nav__dropdown{border:0;padding:0;margin:0;background:transparent}
.site-nav__dropdown>summary{padding-block:.75rem}
.site-nav__dropdown>summary:after{color:currentColor}
.site-nav__submenu a[aria-current="page"]{font-weight:600;background:#e8e4d8}
""")
p=Path('scratch/verificar_visual.cjs')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("await page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-mobile.png',fullPage:true});","await page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-mobile.png',fullPage:true});\nawait page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-mobile-inicio.png'});")
p.write_text(s,encoding='utf-8')

