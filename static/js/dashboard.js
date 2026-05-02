document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('file-input');
  const uploadArea = document.getElementById('upload-area');
  const uploadBtn = document.getElementById('upload-btn');
  const selected = document.getElementById('selected-name');
  const form = document.getElementById('upload-form');
  const errorBox = document.getElementById('upload-error');

  if (!fileInput || !uploadArea) return;
  const browseLabel = uploadArea.querySelector('.link-like');

  const isArchive = (name) => {
    const n = (name || '').toLowerCase();
    return n.endsWith('.zip') || n.endsWith('.rar');
  };

  const showFlash = (message, category = 'error') => {
    const host =
      document.querySelector('.dash-flash') ||
      document.querySelector('.admin-flash') ||
      form?.closest('.card') ||
      document.body;
    if (!host) return;

    const wrap = document.createElement('div');
    wrap.className = 'dash-flash';
    const el = document.createElement('div');
    el.className = `flash ${category}`;
    el.textContent = message;
    wrap.appendChild(el);

    if (host.classList && (host.classList.contains('dash-flash') || host.classList.contains('admin-flash'))) {
      host.appendChild(el);
    } else {
      host.prepend(wrap);
    }

    if (window.__autoDismissFlash) window.__autoDismissFlash(el);
  };

  const setSelected = (name) => {
    selected.textContent = name || '';
    if (browseLabel) browseLabel.textContent = name ? 'Change' : 'browse';
    uploadArea.classList.toggle('has-file', !!name);
    if (!name) {
      uploadBtn.disabled = false;
      if (errorBox) { errorBox.style.display = 'none'; errorBox.textContent=''; }
      return;
    }
    if (!isArchive(name)) {
      uploadBtn.disabled = false;
      if (errorBox) { errorBox.style.display = 'block'; errorBox.textContent = 'Only .zip or .rar files are allowed.'; }
    } else {
      uploadBtn.disabled = false;
      if (errorBox) { errorBox.style.display = 'none'; errorBox.textContent=''; }
    }
  };

  if (uploadBtn) {
    uploadBtn.addEventListener('click', (e) => {
      const f = fileInput.files && fileInput.files[0];
      if (!f) {
        e.preventDefault();
        if (errorBox) { errorBox.style.display = 'block'; errorBox.textContent = 'Please choose a .zip or .rar file to upload.'; }
        showFlash('Please choose a .zip or .rar file to upload.', 'error');
        return;
      }
      if (!isArchive(f.name)) {
        e.preventDefault();
        setSelected(f.name);
        showFlash('Only .zip or .rar files are allowed.', 'error');
      }
    });
  }

  uploadArea.addEventListener('click', () => fileInput.click());
  uploadArea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  fileInput.addEventListener('change', () => {
    const f = fileInput.files && fileInput.files[0];
    setSelected(f ? f.name : '');
  });

  ;['dragenter','dragover','dragleave','drop'].forEach(ev => {
    uploadArea.addEventListener(ev, (e) => { e.preventDefault(); e.stopPropagation(); }, false);
  });
  ;['dragenter','dragover'].forEach(ev => {
    uploadArea.addEventListener(ev, () => uploadArea.classList.add('is-drag'), false);
  });
  ;['dragleave','drop'].forEach(ev => {
    uploadArea.addEventListener(ev, () => uploadArea.classList.remove('is-drag'), false);
  });
  uploadArea.addEventListener('drop', (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      const f = fileInput.files[0];
      setSelected(f ? f.name : '');
    }
  });

  if (form) {
    form.addEventListener('submit', (e) => {
      const f = fileInput.files && fileInput.files[0];
      if (!f || !isArchive(f.name)) {
        e.preventDefault();
        if (!f) {
          if (errorBox) { errorBox.style.display = 'block'; errorBox.textContent = 'Please choose a .zip or .rar file to upload.'; }
          uploadArea.classList.remove('has-file');
          if (browseLabel) browseLabel.textContent = 'browse';
          showFlash('Please choose a .zip or .rar file to upload.', 'error');
          return;
        }
        setSelected(f.name);
        showFlash('Only .zip or .rar files are allowed.', 'error');
      }
    });
  }

  // Normalize initial state (template may render the button disabled)
  setSelected('');
});
