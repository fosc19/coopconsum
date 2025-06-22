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
  
  // SOLUCIÓ DEFINITIVA ACCORDION: Sense scroll jump
  const accordionEl = document.getElementById('dockerGuide');
  
  if (accordionEl) {
    // Interceptar tots els clics en botons accordion
    accordionEl.addEventListener('click', function(e) {
      const button = e.target.closest('.accordion-button');
      if (!button) return;
      
      // Prevenir comportament per defecte completament
      e.preventDefault();
      e.stopPropagation();
      
      // Guardar posició de scroll
      const currentScrollPos = window.pageYOffset;
      
      // Activar mode no-scroll
      document.documentElement.classList.add('accordion-no-scroll');
      
      // Obtenir target del collapse
      const targetId = button.getAttribute('data-bs-target');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        // Gestionar estat del collapse manualment
        const bsCollapse = bootstrap.Collapse.getOrCreateInstance(targetElement, {
          toggle: false
        });
        
        // Toggle del collapse
        if (targetElement.classList.contains('show')) {
          bsCollapse.hide();
        } else {
          bsCollapse.show();
        }
        
        // Actualitzar atributs ARIA manualment
        const isExpanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', !isExpanded);
        
        // Restaurar posició de scroll i desactivar mode no-scroll
        setTimeout(() => {
          window.scrollTo(0, currentScrollPos);
          document.documentElement.classList.remove('accordion-no-scroll');
        }, 100);
      }
    });
  }
  
  // Netejar hash de la URL si existeix
  if (window.location.hash && window.location.hash.match(/^#step\d+$/)) {
    history.replaceState("", document.title, window.location.pathname);
  }
});