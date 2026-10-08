(() => {
  const form = document.getElementById('editor-form');
  if (!form) return;
  const source = document.getElementById('id_conteudo');
  const editor = document.getElementById('editor-visual');
  // Reconstruir somente os elementos permitidos; nunca inserir HTML não confiável.
  const parsed = new DOMParser().parseFromString(source.value, 'text/html');
  const allowed = new Set(['P','DIV','BR','H2','H3','STRONG','B','EM','I','UL','OL','LI','BLOCKQUOTE','A']);
  function copy(node, parent) {
    if (node.nodeType === Node.TEXT_NODE) { parent.append(document.createTextNode(node.textContent)); return; }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    if (['SCRIPT','STYLE','IFRAME','OBJECT'].includes(node.tagName)) return;
    const el = allowed.has(node.tagName) ? document.createElement(node.tagName.toLowerCase()) : parent;
    if (el !== parent) parent.append(el);
    if (node.tagName === 'A') {
      const href = node.getAttribute('href') || '';
      if (/^(https?:|mailto:|\/)/i.test(href)) el.setAttribute('href', href);
    }
    [...node.childNodes].forEach(child => copy(child, el));
  }
  [...parsed.body.childNodes].forEach(node => copy(node, editor));
  editor.hidden = false; source.hidden = true; source.required = false;
  document.getElementById('texto-label').removeAttribute('for');
  const toolbar = document.getElementById('editor-tools'); toolbar.hidden = false;
  toolbar.addEventListener('mousedown', e => { if (e.target.closest('button')) e.preventDefault(); });
  toolbar.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    editor.focus();
    if (b.dataset.block) document.execCommand('formatBlock', false, b.dataset.block);
    else document.execCommand(b.dataset.command, false, null);
    sync();
  });
  function insertText(e, text) { e.preventDefault(); editor.focus(); document.execCommand('insertText', false, text); sync(); }
  editor.addEventListener('paste', e => insertText(e, e.clipboardData.getData('text/plain')));
  editor.addEventListener('drop', e => e.preventDefault());
  let changed = false;
  function sync() { source.value = editor.innerHTML; changed = true; document.getElementById('editor-status').textContent = 'Alterações ainda não salvas.'; }
  editor.addEventListener('input', sync);
  form.addEventListener('change', () => { changed = true; });
  const font = document.getElementById('id_fonte');
  function setFont() { editor.className = 'artigo-corpo-leitura editor-visual fonte-' + font.value; }
  font.addEventListener('change', setFont); setFont();
  const permanence = document.getElementById('id_permanencia');
  function setExpiry() { document.getElementById('expiracao').hidden = permanence.value === 'permanente'; }
  permanence.addEventListener('change', setExpiry); setExpiry();
  form.addEventListener('submit', e => {
    source.value = editor.innerHTML;
    if (!editor.textContent.trim()) { e.preventDefault(); editor.focus(); document.getElementById('editor-status').textContent = 'Escreva o texto do artigo antes de salvar.'; return; }
    changed = false;
  });
  window.addEventListener('beforeunload', e => { if (changed) { e.preventDefault(); e.returnValue = ''; } });
})();
