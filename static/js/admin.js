document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('org-modal');
  const openBtn = document.getElementById('open-org-modal');
  if (!modal || !openBtn) return;

  const open = () => { modal.classList.add('is-open'); modal.setAttribute('aria-hidden', 'false'); };
  const close = () => { modal.classList.remove('is-open'); modal.setAttribute('aria-hidden', 'true'); };

  openBtn.addEventListener('click', open);
  modal.querySelectorAll('[data-close]').forEach(el => el.addEventListener('click', close));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
});
