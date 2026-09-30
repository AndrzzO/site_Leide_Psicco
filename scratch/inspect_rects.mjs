import { spawn } from 'child_process';

const edge = spawn('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', [
  '--headless=new', '--remote-debugging-port=9230', '--disable-gpu', '--no-sandbox', 'about:blank'
]);

setTimeout(async () => {
  const res = await fetch('http://127.0.0.1:9230/json/list');
  const targets = await res.json();
  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  ws.onopen = async () => {
    let id = 1;
    const send = (m, p={}) => new Promise(r => {
      const i = id++;
      const h = e => { const d = JSON.parse(e.data); if (d.id===i) { ws.removeEventListener('message', h); r(d); } };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
    });
    await send('Page.enable');
    const loadPromise = new Promise(r => {
      const lh = e => { const d = JSON.parse(e.data); if (d.method === 'Page.loadEventFired') { ws.removeEventListener('message', lh); r(); } };
      ws.addEventListener('message', lh);
    });
    await send('Page.navigate', { url: 'http://127.0.0.1:8000/' });
    await loadPromise;
    await new Promise(r => setTimeout(r, 1000));
    const info = await send('Runtime.evaluate', {
      expression: `(() => {
        const p = document.getElementById("carrossel-palco").getBoundingClientRect();
        const cards = Array.from(document.querySelectorAll(".carrossel-3d__card")).map(c => {
          const r = c.getBoundingClientRect();
          const cs = window.getComputedStyle(c);
          return {
            title: c.querySelector(".card-foto__titulo")?.textContent,
            rect: { left: Math.round(r.left), top: Math.round(r.top), width: Math.round(r.width) },
            transform: cs.transform,
            left: cs.left,
            marginLeft: cs.marginLeft
          };
        });
        return JSON.stringify({ palco: { left: Math.round(p.left), width: Math.round(p.width), center: Math.round(p.left + p.width/2) }, cards }, null, 2);
      })()`
    });
    console.log(JSON.stringify(info, null, 2));
    ws.close();
    edge.kill();
    process.exit(0);
  };
}, 1500);
