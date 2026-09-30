from pathlib import Path
p=Path('scratch/verificar_visual.cjs')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("fs.mkdirSync('scratch/screenshots_reformulacao',{recursive:true});", """fs.mkdirSync('scratch/screenshots_reformulacao',{recursive:true});
async function loadImages(){
  await page.locator('img').evaluateAll(async imgs => {
    imgs.forEach(i=>i.loading='eager');
    await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));
  });
  await page.evaluate(()=>document.fonts.ready);
}""")
s=s.replace("await page.screenshot({path:", "await loadImages();\nawait page.screenshot({path:")
s=s.replace("await page.setViewportSize({width:390,height:844});", """await page.goto('http://127.0.0.1:8010/',{waitUntil:'networkidle'});
await loadImages();
await page.screenshot({path:'scratch/screenshots_reformulacao/home-primeira-tela.png'});
await page.setViewportSize({width:390,height:844});""")
p.write_text(s,encoding='utf-8')

