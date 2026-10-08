(() => {
  const input = document.getElementById('id_imagem_capa');
  if (!input) return;
  const section = document.getElementById('capa-ajuste');
  const frame = document.getElementById('capa-quadro');
  const image = document.getElementById('capa-previa');
  const x = document.getElementById('id_capa_x');
  const y = document.getElementById('id_capa_y');
  const clear = document.querySelector('[name="imagem_capa-clear"]');
  const original = image.getAttribute('src');
  const initial = [x.value || '50', y.value || '50'];
  let objectURL, drag;
  const clamp = v => Math.round(Math.max(0, Math.min(100, v)));
  function paint(notify = false) {
    image.style.objectPosition = `${x.value === '' ? 50 : x.value}% ${y.value === '' ? 50 : y.value}%`;
    if (notify) {
      x.dispatchEvent(new Event('change', {bubbles:true}));
      document.getElementById('editor-status').textContent = 'Enquadramento alterado. Salve o artigo para confirmar.';
    }
  }
  function excess() {
    const r = frame.getBoundingClientRect();
    const scale = Math.max(r.width / image.naturalWidth, r.height / image.naturalHeight);
    return [Math.max(0, image.naturalWidth * scale - r.width), Math.max(0, image.naturalHeight * scale - r.height)];
  }
  image.addEventListener('load', () => { section.hidden = !!clear?.checked; paint(); });
  image.addEventListener('error', () => { section.hidden = true; });
  input.addEventListener('change', () => {
    if (objectURL) URL.revokeObjectURL(objectURL);
    const file = input.files[0];
    if (file) {
      if (clear) clear.checked = false;
      x.value = y.value = '50';
      objectURL = URL.createObjectURL(file); image.src = objectURL;
    } else if (original) { [x.value, y.value] = initial; image.src = original; }
    else section.hidden = true;
  });
  clear?.addEventListener('change', () => { section.hidden = clear.checked || !image.getAttribute('src'); });
  frame.addEventListener('pointerdown', e => {
    if (e.button !== 0 || !image.naturalWidth) return;
    e.preventDefault(); frame.focus(); frame.setPointerCapture(e.pointerId);
    drag = {id:e.pointerId, px:e.clientX, py:e.clientY, x:Number(x.value || 50), y:Number(y.value || 50), excess:excess()};
    frame.classList.add('arrastando');
  });
  frame.addEventListener('pointermove', e => {
    if (!drag || e.pointerId !== drag.id) return;
    if (drag.excess[0] > 1) x.value = clamp(drag.x - (e.clientX - drag.px) / drag.excess[0] * 100);
    if (drag.excess[1] > 1) y.value = clamp(drag.y - (e.clientY - drag.py) / drag.excess[1] * 100);
    paint(true);
  });
  function stop() { drag = null; frame.classList.remove('arrastando'); }
  frame.addEventListener('pointerup', stop); frame.addEventListener('pointercancel', stop); frame.addEventListener('lostpointercapture', stop);
  frame.addEventListener('keydown', e => {
    const keys = {ArrowLeft:[5,0],ArrowRight:[-5,0],ArrowUp:[0,5],ArrowDown:[0,-5]};
    if (!keys[e.key]) return;
    e.preventDefault(); const extra = excess();
    if (extra[0] > 1) x.value = clamp(Number(x.value || 50) + keys[e.key][0]);
    if (extra[1] > 1) y.value = clamp(Number(y.value || 50) + keys[e.key][1]);
    paint(true);
  });
  document.getElementById('capa-centralizar').addEventListener('click', () => { x.value = y.value = '50'; paint(true); });
  if (original && image.complete && image.naturalWidth) section.hidden = !!clear?.checked;
  paint();
})();
