const { chromium } = require('C:/Users/andre/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
(async()=>{
const browser=await chromium.launch({headless:true,channel:'msedge'});
const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
fs.mkdirSync('scratch/screenshots_reformulacao',{recursive:true});
async function loadImages(){
  await page.locator('img').evaluateAll(async imgs => {
    imgs.forEach(i=>i.loading='eager');
    await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));
  });
  await page.evaluate(()=>document.fonts.ready);
}
const paths={'home':'/','avaliacoes':'/servicos/avaliacao/','burnout':'/servicos/avaliacao/burnout/','bariatrica':'/servicos/avaliacao/cirurgia-bariatrica/','esterilizacao':'/servicos/avaliacao/esterilizacao/','inss':'/servicos/avaliacao/inss/','judicial':'/servicos/avaliacao/processos-judiciais/','ansiedade':'/servicos/avaliacao/ansiedade-depressao/','psicoterapia':'/servicos/psicologia/','credenciamento':'/credenciamento/'};
const reports=[];
for (const [name,path] of Object.entries(paths)) {
const response=await page.goto('http://127.0.0.1:8010'+path,{waitUntil:'networkidle'});
await loadImages();
await page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-desktop.png',fullPage:true});
reports.push({name,status:response.status(),h1:await page.locator('h1').count(),title:await page.title(),brokenImages:await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)),overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
}
await page.goto('http://127.0.0.1:8010/',{waitUntil:'networkidle'});
await loadImages();
await page.screenshot({path:'scratch/screenshots_reformulacao/home-primeira-tela.png'});
await page.setViewportSize({width:390,height:844});
for(const [name,path] of Object.entries(paths)){
await page.goto('http://127.0.0.1:8010'+path,{waitUntil:'networkidle'});
await loadImages();
await page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-mobile.png',fullPage:true});
await page.screenshot({path:'scratch/screenshots_reformulacao/'+name+'-mobile-inicio.png'});
reports.push({name,mobile:true,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
}
await page.goto('http://127.0.0.1:8010/',{waitUntil:'networkidle'});
await page.locator('[data-menu-toggle]').click();
await page.locator('#menu-mobile-painel summary').click();
await loadImages();
await page.screenshot({path:'scratch/screenshots_reformulacao/menu-mobile.png',fullPage:false});
reports.push({menuExpanded:await page.locator('[data-menu-toggle]').getAttribute('aria-expanded'),submenuVisible:await page.locator('#menu-mobile-painel a[href="/servicos/avaliacao/inss/"]').isVisible()});
await page.keyboard.press('Escape');
reports.push({submenuClosed:await page.locator('#menu-mobile-painel details').evaluate(el=>!el.open)});
await page.keyboard.press('Escape');
reports.push({menuClosed:await page.locator('[data-menu-toggle]').getAttribute('aria-expanded')});
fs.writeFileSync('scratch/screenshots_reformulacao/verificacao.json',JSON.stringify(reports,null,2));
console.log(JSON.stringify(reports,null,2));
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
