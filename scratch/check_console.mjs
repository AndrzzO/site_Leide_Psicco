import { spawn } from 'child_process';

const edge = spawn('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', [
  '--headless=new', '--remote-debugging-port=9233', '--disable-gpu', '--no-sandbox', 'about:blank'
]);

setTimeout(async () => {
  try {
    const res = await fetch('http://127.0.0.1:9233/json/list');
    const targets = await res.json();
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const send = (m, p={}) => new Promise(r => {
      const i = id++;
      const h = e => { const d = JSON.parse(e.data); if (d.id===i) { ws.removeEventListener('message', h); r(d); } };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
    });

    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.method === 'Console.messageAdded' || d.method === 'Runtime.consoleAPICalled') {
        console.log('CONSOLE:', d.params);
      }
      if (d.method === 'Runtime.exceptionThrown') {
        console.error('EXCEPTION:', d.params.exceptionDetails);
      }
    };

    await new Promise(r => ws.onopen = r);
    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8000/' });
    await new Promise(r => setTimeout(r, 2000));

    const check = await send('Runtime.evaluate', {
      returnByValue: true,
      expression: `(() => {
        const dots = document.querySelectorAll(".carrossel-3d__dot");
        const activeCard = document.querySelector(".carrossel-3d__card--ativo");
        const cards = document.querySelectorAll(".carrossel-3d__card");
        return {
          totalCards: cards.length,
          totalDots: dots.length,
          activeCard: activeCard ? activeCard.getAttribute("data-indice") : "NONE",
          cardClasses: Array.from(cards).map(c => c.className)
        };
      })()`
    });
    console.log('DOM check result:', check.result.result.value);

    // Click Next
    await send('Runtime.evaluate', { expression: 'document.getElementById("carrossel-proximo").click()' });
    await new Promise(r => setTimeout(r, 200));
    const nextCheck = await send('Runtime.evaluate', {
      returnByValue: true,
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('After Next click, active card index:', nextCheck.result.result.value);

    // Mouse Wheel
    await send('Runtime.evaluate', {
      expression: `document.getElementById("carrossel-areas").dispatchEvent(new WheelEvent("wheel", { deltaY: 50, bubbles: true, cancelable: true }))`
    });
    await new Promise(r => setTimeout(r, 450));
    const wheelCheck = await send('Runtime.evaluate', {
      returnByValue: true,
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('After Wheel, active card index:', wheelCheck.result.result.value);

    // Click Dot 0
    await send('Runtime.evaluate', { expression: 'document.querySelectorAll(".carrossel-3d__dot")[0].click()' });
    await new Promise(r => setTimeout(r, 200));
    const dotCheck = await send('Runtime.evaluate', {
      returnByValue: true,
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('After Dot 0 click, active card index:', dotCheck.result.result.value);

    ws.close();
    edge.kill();
    process.exit(0);
  } catch (err) {
    console.error(err);
    edge.kill();
    process.exit(1);
  }
}, 1500);
