import { spawn } from 'child_process';
import fs from 'fs';

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const port = 9226;

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
  await sleep(2000);

  // Desktop screenshot
  await send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });
  await sleep(500);

  const desktopScreenshot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
  fs.writeFileSync('scratch/screenshot_desktop.jpg', Buffer.from(desktopScreenshot.result.data, 'base64'));

  // Mobile screenshot
  await send('Emulation.setDeviceMetricsOverride', {
    width: 390,
    height: 844,
    deviceScaleFactor: 2,
    mobile: true
  });
  await sleep(500);

  const mobileScreenshot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
  fs.writeFileSync('scratch/screenshot_mobile.jpg', Buffer.from(mobileScreenshot.result.data, 'base64'));

  console.log('Screenshots saved successfully!');

  ws.close();
  edge.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  edge.kill();
  process.exit(1);
});
