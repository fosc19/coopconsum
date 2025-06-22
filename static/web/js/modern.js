/**
 * Civada - Funcionalidades modernas para la web
 */

document.addEventListener('DOMContentLoaded', function() {
  // Menú de navegación con efecto al hacer scroll
  const menu = document.querySelector('.civada-menu');
  const header = document.querySelector('.civada-header');
  
  if (menu && header) {
    const headerHeight = header.offsetHeight;
    
    window.addEventListener('scroll', function() {
      if (window.scrollY > headerHeight) {
        menu.classList.add('scrolled');
      } else {
        menu.classList.remove('scrolled');
      }
    });
  }
  
  // Animación de elementos al entrar en el viewport
  const animateElements = document.querySelectorAll('.animate-on-scroll');
  
  if (animateElements.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fade-in');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1
    });
    
    animateElements.forEach(element => {
      observer.observe(element);
    });
  }
  
  // Inicialización de tooltips (requiere Bootstrap)
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  if (tooltipTriggerList.length > 0) {
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
  
  // Mejora de imágenes con lazy loading
  const images = document.querySelectorAll('img:not([loading])');
  images.forEach(img => {
    img.setAttribute('loading', 'lazy');
  });
  
  // Botón para volver arriba
  const createBackToTopButton = () => {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'back-to-top';
    button.setAttribute('aria-label', 'Volver arriba');
    document.body.appendChild(button);
    
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        button.classList.add('show');
      } else {
        button.classList.remove('show');
      }
    });
    
    button.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  };
  
  createBackToTopButton();
  
  // FIX COMPLET ACCORDION: Prevenir scroll jump amb events Bootstrap
  const accordionEl = document.getElementById('dockerGuide');
  
  if (accordionEl) {
    let savedPosition = 0;
    
    // Interceptar events de Bootstrap
    accordionEl.addEventListener('show.bs.collapse', function(e) {
      savedPosition = window.pageYOffset;
      document.documentElement.classList.add('accordion-animating');
    });
    
    accordionEl.addEventListener('shown.bs.collapse', function(e) {
      window.scrollTo(0, savedPosition);
      document.documentElement.classList.remove('accordion-animating');
    });
    
    accordionEl.addEventListener('hide.bs.collapse', function(e) {
      savedPosition = window.pageYOffset;
      document.documentElement.classList.add('accordion-animating');
    });
    
    accordionEl.addEventListener('hidden.bs.collapse', function(e) {
      window.scrollTo(0, savedPosition);
      document.documentElement.classList.remove('accordion-animating');
    });
    
    // Opció alternativa: Control manual de clics
    const accordionButtons = accordionEl.querySelectorAll('.accordion-button');
    accordionButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        const scrollPos = window.pageYOffset;
        const targetId = this.getAttribute('data-bs-target');
        const targetEl = document.querySelector(targetId);
        
        if (targetEl) {
          // Prevenir comportament per defecte només si cal
          setTimeout(() => {
            if (Math.abs(window.pageYOffset - scrollPos) > 50) {
              window.scrollTo(0, scrollPos);
            }
          }, 10);
        }
      });
    });
  }
  
  // Netejar URL si té hash al carregar
  if (window.location.hash && window.location.hash.match(/^#step\d+$/)) {
    history.replaceState("", document.title, window.location.pathname);
  }
  
  // Prevenir navegació per hash
  window.addEventListener('hashchange', function(e) {
    if (location.hash && location.hash.match(/^#step\d+$/)) {
      e.preventDefault();
      history.pushState("", document.title, window.location.pathname + window.location.search);
      return false;
    }
  });
});