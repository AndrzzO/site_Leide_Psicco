import { spawn } from 'child_process';

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const port = 9225;

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

  await send('Page.enable');
  await send('Page.navigate', { url: 'http://127.0.0.1:8000/' });
  await sleep(1500);

  await send('Emulation.setDeviceMetricsOverride', {
    width: 390,
    height: 844,
    deviceScaleFactor: 1,
    mobile: true
  });
  await sleep(300);

  // Click hamburger button to open drawer
  await send('Runtime.evaluate', {
    expression: `(() => {
      const toggle = document.querySelector('[data-menu-toggle]');
      toggle.click();
    })()`
  });
  await sleep(400);

  // Check state when open
  const openRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const docEl = document.documentElement;
      const panel = document.querySelector('[data-menu-panel]');
      return {
        clientWidth: docEl.clientWidth,
        scrollWidth: docEl.scrollWidth,
        hasHorizontalScroll: docEl.scrollWidth > docEl.clientWidth,
        menuAbertoClass: panel.classList.contains('menu-aberto'),
        menuVisibility: getComputedStyle(panel).visibility,
        menuRight: panel.getBoundingClientRect().right
      };
    })()`,
    returnByValue: true
  });
  console.log('Open state:', openRes.result?.result?.value);

  // Click to close
  await send('Runtime.evaluate', {
    expression: `(() => {
      const toggle = document.querySelector('[data-menu-toggle]');
      toggle.click();
    })()`
  });
  await sleep(400);

  // Check state when closed
  const closeRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const docEl = document.documentElement;
      const panel = document.querySelector('[data-menu-panel]');
      return {
        clientWidth: docEl.clientWidth,
        scrollWidth: docEl.scrollWidth,
        hasHorizontalScroll: docEl.scrollWidth > docEl.clientWidth,
        menuAbertoClass: panel.classList.contains('menu-aberto'),
        hiddenAttr: panel.hasAttribute('hidden')
      };
    })()`,
    returnByValue: true
  });
  console.log('Closed state:', closeRes.result?.result?.value);

  ws.close();
  edge.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  edge.kill();
  process.exit(1);
});
