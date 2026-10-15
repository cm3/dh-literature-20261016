(() => {
  'use strict';
  const zoom = document.querySelector('#plan-zoom');
  zoom?.addEventListener('change', () => {
    const viewport = document.querySelector('.plan-viewport');
    viewport.classList.toggle('is-zoomed', Number(zoom.value) > 1);
    viewport.querySelector('svg').style.width = `${Number(zoom.value) * 100}%`;
  });
  const mode = document.querySelector('#reading-mode');
  const panel = document.querySelector('#reading-note');
  const passages = [...document.querySelectorAll('.passage[data-note-id]')].filter(p => p.dataset.noteId);
  const dialog = document.querySelector('#mix-dialog');
  if (!panel || !mode) return; // Overview, people, and schematic are independent pages.
  let current = '', pinned = null, dismissed = '', scheduled = false;
  function showNote(id) {
    if (id === current) return;
    current = id;
    if (!id) { panel.hidden = true; panel.replaceChildren(); return; }
    const source = document.getElementById('note-' + id);
    if (!source) return;
    panel.replaceChildren(source.content.cloneNode(true));
    const close = document.createElement('button');
    close.className = 'note-dismiss'; close.textContent = '閉じる ×'; close.setAttribute('aria-label', '読書注を閉じる');
    close.addEventListener('click', () => { dismissed = id; pinned = null; showNote(''); });
    panel.prepend(close); panel.hidden = false; panel.parentElement.scrollTop = 0;
  }
  function visible(p) {
    const r = p.getBoundingClientRect();
    return r.bottom > innerHeight * .21 && r.top < innerHeight * .77;
  }
  function update() {
    scheduled = false;
    const choices = passages.filter(visible);
    if (pinned && !visible(pinned)) pinned = null;
    const target = innerHeight * .37;
    choices.sort((a, b) => {
      function distance(el) { const r = el.getBoundingClientRect(); return r.top <= target && r.bottom >= target ? 0 : Math.min(Math.abs(r.top - target), Math.abs(r.bottom - target)); }
      return distance(a) - distance(b);
    });
    const id = (pinned || choices[0])?.dataset.noteId || '';
    if (dismissed && !choices.some(p => p.dataset.noteId === dismissed)) dismissed = '';
    showNote(id === dismissed ? '' : id);
    const total = document.documentElement.scrollHeight - innerHeight;
    document.querySelector('#progress-bar').style.transform = `scaleX(${total > 0 ? Math.max(0, Math.min(1, scrollY / total)) : 0})`;
  }
  function schedule() { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }
  function applyMode(value) {
    document.body.dataset.mode = value;
    document.querySelectorAll('details.english').forEach(el => { el.open = value !== 'ja'; });
    schedule();
  }
  mode.addEventListener('change', () => { applyMode(mode.value); });
  document.addEventListener('click', event => {
    const note = event.target.closest('[data-note]');
    if (note) { pinned = note.closest('.passage'); dismissed = ''; showNote(note.dataset.note); }
    const trigger = event.target.closest('[data-window]');
    if (trigger) {
      const template = document.getElementById('window-' + trigger.dataset.window);
      if (!template) return;
      const content = document.querySelector('#dialog-body'); content.replaceChildren(template.content.cloneNode(true));
      content.querySelector('h2').id = 'mix-dialog-title'; dialog.showModal(); dialog.scrollTop = 0;
    }
    if (event.target.closest('.return-context')) { dialog.close(); schedule(); }
  });
  document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  document.querySelectorAll('details').forEach(el => el.addEventListener('toggle', schedule));
  window.addEventListener('hashchange', schedule);
  applyMode('ja');
})();
