import { spawn } from 'child_process';

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const port = 9223;

const edge = spawn(edgePath, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  '--disable-gpu',
  '--no-sandbox',
  'about:blank'
]);

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  await sleep(1500);

  const targetsRes = await fetch(`http://127.0.0.1:${port}/json/list`);
  const targets = await targetsRes.json();
  const pageTarget = targets.find(t => t.type === 'page') || targets[0];

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      pending.get(data.id)(data);
      pending.delete(data.id);
    }
  };

  function send(method, params = {}) {
    return new Promise((resolve) => {
      const id = idCounter++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await new Promise(r => ws.onopen = r);

  const routes = [
    '/',
    '/sobre-mim/',
    '/servicos/psicologia/',
    '/servicos/traumas/',
    '/servicos/separacao-e-recomecos/',
    '/servicos/novos-relacionamentos/',
    '/servicos/avaliacao/',
    '/conteudos/',
    '/contato/',
    '/politica-de-privacidade/'
  ];

  const viewports = [
    { width: 360, height: 740, name: 'Android Galaxy' },
    { width: 390, height: 844, name: 'iPhone 12/13/14' },
    { width: 768, height: 1024, name: 'Tablet 768' },
    { width: 1024, height: 768, name: 'iPad Pro / Laptop' },
    { width: 1280, height: 800, name: 'MacBook 1280' },
    { width: 1440, height: 900, name: 'Desktop 1440' },
    { width: 1920, height: 1080, name: 'Full HD 1920' }
  ];

  for (const route of routes) {
    console.log(`\n========================================`);
    console.log(`TESTING ROUTE: ${route}`);
    console.log(`========================================`);
    await send('Page.navigate', { url: `http://127.0.0.1:8000${route}` });
    await sleep(1000);

    await sleep(200);

    for (const vp of viewports) {
      await send('Emulation.setDeviceMetricsOverride', {
        width: vp.width,
        height: vp.height,
        deviceScaleFactor: 1,
        mobile: vp.width < 768
      });
      await sleep(150);

      const evalRes = await send('Runtime.evaluate', {
        expression: `(() => {
          const docEl = document.documentElement;
          const scrollWidth = docEl.scrollWidth;
          const clientWidth = docEl.clientWidth;
          return {
            viewport: '${vp.name}',
            clientWidth,
            scrollWidth,
            hasHorizontalScroll: scrollWidth > clientWidth
          };
        })()`,
        returnByValue: true
      });
      const val = evalRes.result?.result?.value;
      console.log(`  ${val.viewport}: clientWidth=${val.clientWidth}, scrollWidth=${val.scrollWidth}, hasHorizontalScroll=${val.hasHorizontalScroll}`);
    }
  }
  ws.close();
  edge.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  edge.kill();
  process.exit(1);
});
