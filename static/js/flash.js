document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash");
  if (!flashes.length) return;

  const hideAfterMs = 4500;
  const animationMs = 250;

  flashes.forEach((el) => {
    window.setTimeout(() => {
      el.classList.add("flash--hide");
      window.setTimeout(() => {
        el.remove();
      }, animationMs + 50);
    }, hideAfterMs);
  });
});

window.__autoDismissFlash = (el, opts) => {
  if (!el) return;
  const hideAfterMs = (opts && opts.hideAfterMs) || 4500;
  const animationMs = (opts && opts.animationMs) || 250;
  window.setTimeout(() => {
    el.classList.add("flash--hide");
    window.setTimeout(() => el.remove(), animationMs + 50);
  }, hideAfterMs);
};
