document.addEventListener('DOMContentLoaded', function () {
  const dropdowns = document.querySelectorAll('.nav-item.dropdown');
  const defaultHeader = document.getElementById('default-header');
  const heroHeader = document.getElementById('hero-header');
  const main = document.getElementById('main-content');
  const activeHeader = heroHeader || defaultHeader;

  // Dropdown hover behavior
  dropdowns.forEach(dropdown => {
    const menu = dropdown.querySelector('.dropdown-menu');

    dropdown.addEventListener('mouseenter', function () {
      clearTimeout(this._timer);
      menu.style.transitionDelay = '0s';
      menu.style.opacity = '1';
      menu.style.visibility = 'visible';
      menu.style.transform = 'translateY(0)';
      menu.style.pointerEvents = 'auto';
    });

    dropdown.addEventListener('mouseleave', function () {
      this._timer = setTimeout(() => {
        menu.style.opacity = '0';
        menu.style.visibility = 'hidden';
        menu.style.transform = 'translateY(10px)';
        menu.style.pointerEvents = 'none';
      }, 100);
    });

    menu.addEventListener('mouseenter', function () {
      clearTimeout(dropdown._timer);
    });

    menu.addEventListener('mouseleave', function () {
      dropdown._timer = setTimeout(() => {
        menu.style.opacity = '0';
        menu.style.visibility = 'hidden';
        menu.style.transform = 'translateY(10px)';
        menu.style.pointerEvents = 'none';
      }, 100);
    });
  });

  // Toggle which header is shown
  if (heroHeader) {
    if (defaultHeader) defaultHeader.style.display = 'none';
    heroHeader.style.display = 'flex';
    if (main) main.style.paddingTop = '0';
  } else {
    if (defaultHeader) defaultHeader.style.display = 'flex';
    if (main) main.style.paddingTop = '7rem';
  }

  // Handle hamburger menu dynamically for activeHeader
  if (activeHeader) {
    const hamburger = activeHeader.querySelector('#hamburger');
    const mobileNav = activeHeader.querySelector('#mobile-nav');
    const closeBtn = activeHeader.querySelector('#close-btn');

    if (hamburger && mobileNav && closeBtn) {
      hamburger.addEventListener('click', () => {
        mobileNav.classList.add('active');
        hamburger.style.display = 'none';
      });

      closeBtn.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        hamburger.style.display = 'block';
      });

      // Toggle submenu in mobile nav
      const mobileDropdowns = activeHeader.querySelectorAll('.dropdown-toggle');
      mobileDropdowns.forEach(item => {
        item.addEventListener('click', () => {
          item.classList.toggle('active');
        });
      });
    }
  }

  // Sticky scroll behavior
  if (activeHeader) {
    const logo = document.getElementById('logo');
    const whiteLogo = logo?.getAttribute('data-logo-white');
    const coloredLogo = logo?.getAttribute('data-logo-colored');

    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        activeHeader.classList.add('scrolled');
        if (logo && coloredLogo) logo.src = coloredLogo;
      } else {
        activeHeader.classList.remove('scrolled');
        if (logo && whiteLogo) logo.src = whiteLogo;
      }
    });
  }
});
