window.addEventListener('scroll', function () {
  const header = document.querySelector('.header');
  const logo = document.getElementById('logo');

  if (header && logo) {
    const whiteLogo = logo.getAttribute('data-logo-white');
    const coloredLogo = logo.getAttribute('data-logo-colored');

    if (window.scrollY > 50) {
      header.classList.add('scrolled');
      logo.src = coloredLogo;
    } else {
      header.classList.remove('scrolled');
      logo.src = whiteLogo;
    }
  }
});
