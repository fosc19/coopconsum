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
  
  // SOLUCIÓ ULTRA-ROBUSTA ACCORDION: Evitar scroll a "Necessites ajuda"
  const accordionEl = document.getElementById('dockerGuide');
  
  if (accordionEl) {
    let savedScrollPosition = 0;
    let isAccordionOperating = false;
    
    // Force scroll position múltiples vegades durant la transició
    function forceScrollPosition(position, duration = 500) {
      const startTime = Date.now();
      const forceScroll = () => {
        window.scrollTo(0, position);
        if (Date.now() - startTime < duration) {
          requestAnimationFrame(forceScroll);
        }
      };
      forceScroll();
    }
    
    // Interceptor d'events Bootstrap per detectar canvis
    accordionEl.addEventListener('show.bs.collapse', function(e) {
      savedScrollPosition = window.pageYOffset;
      isAccordionOperating = true;
      document.documentElement.classList.add('accordion-no-scroll');
    });
    
    accordionEl.addEventListener('shown.bs.collapse', function(e) {
      forceScrollPosition(savedScrollPosition, 300);
      setTimeout(() => {
        document.documentElement.classList.remove('accordion-no-scroll');
        isAccordionOperating = false;
      }, 400);
    });
    
    accordionEl.addEventListener('hide.bs.collapse', function(e) {
      savedScrollPosition = window.pageYOffset;
      isAccordionOperating = true;
      document.documentElement.classList.add('accordion-no-scroll');
    });
    
    accordionEl.addEventListener('hidden.bs.collapse', function(e) {
      forceScrollPosition(savedScrollPosition, 300);
      setTimeout(() => {
        document.documentElement.classList.remove('accordion-no-scroll');
        isAccordionOperating = false;
      }, 400);
    });
    
    // Interceptar clics directament en botons
    const accordionButtons = accordionEl.querySelectorAll('.accordion-button');
    accordionButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        savedScrollPosition = window.pageYOffset;
        isAccordionOperating = true;
        
        // Forçar posició cada 50ms durant 1 segon
        let attempts = 0;
        const maxAttempts = 20;
        const intervalId = setInterval(() => {
          window.scrollTo(0, savedScrollPosition);
          attempts++;
          if (attempts >= maxAttempts || !isAccordionOperating) {
            clearInterval(intervalId);
          }
        }, 50);
      });
    });
    
    // Observer per detectar canvis de layout
    const observer = new MutationObserver((mutations) => {
      if (isAccordionOperating) {
        mutations.forEach((mutation) => {
          if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
            // Força scroll quan detecta canvis de classe en accordion-items
            window.scrollTo(0, savedScrollPosition);
          }
        });
      }
    });
    
    // Observar canvis en tots els accordion-items
    const accordionItems = accordionEl.querySelectorAll('.accordion-collapse');
    accordionItems.forEach(item => {
      observer.observe(item, { attributes: true, attributeFilter: ['class'] });
    });
  }
  
  // Prevenir QUALSEVOL scroll automàtic a hashs
  if (window.location.hash) {
    history.replaceState("", document.title, window.location.pathname);
  }
  
  // Interceptar tots els canvis de hash
  window.addEventListener('hashchange', function(e) {
    e.preventDefault();
    history.replaceState("", document.title, window.location.pathname);
    return false;
  });
});