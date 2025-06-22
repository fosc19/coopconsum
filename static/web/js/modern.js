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
  
  // Fix per accordions: prevenir scroll automàtic
  const accordionButtons = document.querySelectorAll('.accordion-button');
  
  accordionButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      // Guardar la posició actual del scroll
      const currentScrollPosition = window.pageYOffset;
      
      // Esperar que l'accordion s'obri/tanqui
      setTimeout(() => {
        // Restaurar la posició de scroll si ha canviat automàticament
        if (Math.abs(window.pageYOffset - currentScrollPosition) > 100) {
          window.scrollTo({
            top: currentScrollPosition,
            behavior: 'auto'
          });
        }
      }, 50);
    });
  });
  
  // Alternative: Interceptar canvis de hash que poden causar scroll
  window.addEventListener('hashchange', function(e) {
    // Si el hash és un step d'accordion, prevenir scroll
    if (window.location.hash.match(/^#step\d+$/)) {
      e.preventDefault();
      history.replaceState(null, null, ' ');
    }
  });
});