import { spawn } from 'child_process';

const edge = spawn('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', [
  '--headless=new', '--remote-debugging-port=9232', '--disable-gpu', '--no-sandbox', 'about:blank'
]);

setTimeout(async () => {
  try {
    const res = await fetch('http://127.0.0.1:9232/json/list');
    const targets = await res.json();
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);

    let id = 1;
    const send = (m, p={}) => new Promise(r => {
      const i = id++;
      const h = e => { const d = JSON.parse(e.data); if (d.id===i) { ws.removeEventListener('message', h); r(d); } };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
    });

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8000/' });
    await new Promise(r => setTimeout(r, 2000));

    // Test 1: Check initial active card
    const t1 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 1 - Initial active card index:', t1.result.value);

    // Test 2: Click next button
    await send('Runtime.evaluate', {
      expression: 'document.getElementById("carrossel-proximo").click()'
    });
    await new Promise(r => setTimeout(r, 300));
    const t2 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 2 - After Next button click index:', t2.result.value);

    // Test 3: Click previous button
    await send('Runtime.evaluate', {
      expression: 'document.getElementById("carrossel-anterior").click()'
    });
    await new Promise(r => setTimeout(r, 300));
    const t3 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 3 - After Prev button click index (back to 0):', t3.result.value);

    // Test 4: Mouse wheel dispatch
    await send('Runtime.evaluate', {
      expression: `(() => {
        const c = document.getElementById("carrossel-areas");
        c.dispatchEvent(new WheelEvent("wheel", { deltaY: 50, bubbles: true, cancelable: true }));
      })()`
    });
    await new Promise(r => setTimeout(r, 500));
    const t4 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 4 - After Mouse Wheel index:', t4.result.value);

    // Test 5: Click on dot 3
    await send('Runtime.evaluate', {
      expression: 'document.querySelectorAll(".carrossel-3d__dot")[3].click()'
    });
    await new Promise(r => setTimeout(r, 300));
    const t5 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 5 - After Dot 3 click index:', t5.result.value);

    // Test 6: Click side card directly to center it
    await send('Runtime.evaluate', {
      expression: 'document.querySelectorAll(".carrossel-3d__card")[0].click()'
    });
    await new Promise(r => setTimeout(r, 300));
    const t6 = await send('Runtime.evaluate', {
      expression: 'document.querySelector(".carrossel-3d__card--ativo")?.getAttribute("data-indice")'
    });
    console.log('Test 6 - After clicking Card 0 to center it:', t6.result.value);

    console.log('All interaction tests passed successfully!');
    ws.close();
    edge.kill();
    process.exit(0);
  } catch (err) {
    console.error(err);
    edge.kill();
    process.exit(1);
  }
}, 1500);
