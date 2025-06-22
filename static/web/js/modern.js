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
  
  // SOLUCIÓ COMPLETA PER L'SCROLL JUMP DELS ACCORDIONS - MULTI-CAPA
  const accordionContainer = document.getElementById('dockerGuide');
  if (!accordionContainer) return;

  // Variables globals per mantenir l'estat
  let isAccordionAnimating = false;
  let lastKnownScrollPosition = 0;
  let scrollLockTimeout = null;
  
  // FUNCIÓ per bloquejar l'scroll completament
  function lockScroll() {
    // Guarda la posició actual
    lastKnownScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
    
    // Mètode 1: Overflow hidden amb compensació
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = scrollbarWidth + 'px';
    
    // Mètode 2: Fixed positioning
    document.body.style.position = 'fixed';
    document.body.style.top = `-${lastKnownScrollPosition}px`;
    document.body.style.width = '100%';
    
    isAccordionAnimating = true;
  }
  
  // FUNCIÓ per desbloquejar l'scroll
  function unlockScroll() {
    // Restaura els estils
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    
    // Restaura la posició
    window.scrollTo(0, lastKnownScrollPosition);
    
    // Força la posició diverses vegades per assegurar-nos
    let attempts = 0;
    const forcePosition = setInterval(() => {
      window.scrollTo(0, lastKnownScrollPosition);
      attempts++;
      if (attempts > 10) {
        clearInterval(forcePosition);
        isAccordionAnimating = false;
      }
    }, 10);
  }
  
  // INTERCEPTA tots els clicks als botons d'accordion
  const accordionButtons = accordionContainer.querySelectorAll('.accordion-button');
  
  accordionButtons.forEach(button => {
    // Elimina els event listeners existents de Bootstrap
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);
    
    // Afegeix el nostre handler personalitzat
    newButton.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      // Obté l'element target
      const targetId = this.getAttribute('data-bs-target');
      const targetElement = document.querySelector(targetId);
      
      if (!targetElement) return;
      
      // Bloqueja l'scroll ABANS de fer res més
      lockScroll();
      
      // Gestiona l'accordion manualment
      const isCurrentlyOpen = targetElement.classList.contains('show');
      
      // Tanca tots els altres accordions (si cal)
      const allCollapses = accordionContainer.querySelectorAll('.accordion-collapse');
      allCollapses.forEach(collapse => {
        if (collapse !== targetElement && collapse.classList.contains('show')) {
          collapse.classList.remove('show');
          collapse.previousElementSibling.querySelector('.accordion-button').classList.add('collapsed');
          collapse.previousElementSibling.querySelector('.accordion-button').setAttribute('aria-expanded', 'false');
        }
      });
      
      // Toggle l'accordion actual
      if (isCurrentlyOpen) {
        targetElement.classList.remove('show');
        this.classList.add('collapsed');
        this.setAttribute('aria-expanded', 'false');
      } else {
        targetElement.classList.add('show');
        this.classList.remove('collapsed');
        this.setAttribute('aria-expanded', 'true');
      }
      
      // Desbloqueja l'scroll després de l'animació
      clearTimeout(scrollLockTimeout);
      scrollLockTimeout = setTimeout(() => {
        unlockScroll();
      }, 350); // Durada de l'animació de Bootstrap
    });
  });
  
  // PREVENIR scroll durant l'animació
  function preventScroll(e) {
    if (isAccordionAnimating) {
      e.preventDefault();
      e.stopPropagation();
      window.scrollTo(0, lastKnownScrollPosition);
      return false;
    }
  }
  
  // Afegeix listeners per prevenir scroll
  window.addEventListener('scroll', preventScroll, { passive: false });
  window.addEventListener('wheel', preventScroll, { passive: false });
  window.addEventListener('touchmove', preventScroll, { passive: false });
  
  // GESTIÓ DE HASH/ANCHOR LINKS
  window.addEventListener('hashchange', function(e) {
    if (isAccordionAnimating) {
      e.preventDefault();
      e.stopPropagation();
      history.pushState("", document.title, window.location.pathname + window.location.search);
      window.scrollTo(0, lastKnownScrollPosition);
      return false;
    }
  }, true);
  
  // OBSERVER per detectar canvis al DOM que puguin causar scroll
  const scrollObserver = new MutationObserver(function(mutations) {
    if (isAccordionAnimating) {
      window.scrollTo(0, lastKnownScrollPosition);
    }
  });
  
  // Observa canvis al body i html
  scrollObserver.observe(document.body, {
    attributes: true,
    childList: true,
    subtree: true,
    attributeFilter: ['class', 'style']
  });
  
  // FALLBACK: Força la posició cada frame durant l'animació
  accordionContainer.addEventListener('click', function(e) {
    if (e.target.closest('.accordion-button')) {
      const savedPos = window.pageYOffset;
      let frameCount = 0;
      
      function forceScrollPosition() {
        if (frameCount < 60) { // ~1 segon a 60fps
          window.scrollTo(0, savedPos);
          frameCount++;
          requestAnimationFrame(forceScrollPosition);
        }
      }
      
      requestAnimationFrame(forceScrollPosition);
    }
  });
  
  // CLEAN UP quan es descarrega la pàgina
  window.addEventListener('beforeunload', function() {
    if (scrollObserver) {
      scrollObserver.disconnect();
    }
    clearTimeout(scrollLockTimeout);
  });
});