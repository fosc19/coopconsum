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
  
  // WIZARD/STEPPER NAVEGACIÓ AMB SCROLL LOCK
  const wizardContainer = document.getElementById('dockerWizard');
  if (wizardContainer) {
    let currentStep = 1;
    const totalSteps = 4;
    let savedScrollPosition = 0;
    
    // Funcions globals per la navegació amb SCROLL LOCK ULTRA AGRESSIU
    window.changeStep = function(direction) {
      const newStep = currentStep + direction;
      
      if (newStep >= 1 && newStep <= totalSteps) {
        // GUARDAR posició actual
        savedScrollPosition = window.pageYOffset;
        
        // BLOQUEJAR SCROLL COMPLETAMENT
        lockScrollCompletely();
        
        // Canviar step
        showStep(newStep);
        
        // RESTAURAR després d'un temps
        setTimeout(() => {
          unlockScrollCompletely();
        }, 100);
      }
    };
    
    function lockScrollCompletely() {
      // Mètode 1: Overflow hidden
      document.body.style.overflow = 'hidden';
      document.documentElement.style.overflow = 'hidden';
      
      // Mètode 2: Position fixed
      const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
      document.body.style.position = 'fixed';
      document.body.style.top = `-${savedScrollPosition}px`;
      document.body.style.width = '100%';
      document.body.style.paddingRight = scrollbarWidth + 'px';
      
      // Mètode 3: Prevenir events
      document.addEventListener('wheel', preventDefault, { passive: false });
      document.addEventListener('touchmove', preventDefault, { passive: false });
      document.addEventListener('scroll', preventDefault, { passive: false });
    }
    
    function unlockScrollCompletely() {
      // Restaurar estils
      document.body.style.overflow = '';
      document.documentElement.style.overflow = '';
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      document.body.style.paddingRight = '';
      
      // Eliminar event listeners
      document.removeEventListener('wheel', preventDefault);
      document.removeEventListener('touchmove', preventDefault);
      document.removeEventListener('scroll', preventDefault);
      
      // SCROLL SUAU cap al wizard
      const wizardAnchor = document.getElementById('wizardAnchor');
      if (wizardAnchor) {
        wizardAnchor.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start',
          inline: 'nearest'
        });
      } else {
        // Fallback: restaurar posició original
        window.scrollTo(0, savedScrollPosition);
      }
    }
    
    function preventDefault(e) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
    
    function showStep(stepNumber) {
      // Amaga tots els steps
      const allSteps = wizardContainer.querySelectorAll('.wizard-step-content');
      allSteps.forEach(step => step.classList.remove('active'));
      
      // Mostra el step actual
      const currentStepElement = document.getElementById(`step${stepNumber}`);
      if (currentStepElement) {
        currentStepElement.classList.add('active');
      }
      
      // Actualitza indicadors de progrés
      updateProgress(stepNumber);
      
      // Actualitza botons de navegació
      updateNavigationButtons(stepNumber);
      
      currentStep = stepNumber;
    }
    
    function updateProgress(stepNumber) {
      // Actualitza barra de progrés
      const progressBar = document.getElementById('progressBar');
      if (progressBar) {
        const percentage = (stepNumber / totalSteps) * 100;
        progressBar.style.width = `${percentage}%`;
      }
      
      // Actualitza indicadors de steps
      const stepIndicators = wizardContainer.querySelectorAll('.wizard-step');
      stepIndicators.forEach((indicator, index) => {
        if (index + 1 <= stepNumber) {
          indicator.classList.add('active');
        } else {
          indicator.classList.remove('active');
        }
      });
    }
    
    function updateNavigationButtons(stepNumber) {
      const prevBtn = document.getElementById('prevBtn');
      const nextBtn = document.getElementById('nextBtn');
      
      if (prevBtn) {
        prevBtn.disabled = (stepNumber === 1);
      }
      
      if (nextBtn) {
        if (stepNumber === totalSteps) {
          nextBtn.innerHTML = '<i class="fas fa-check me-2"></i>Finalitzar';
          nextBtn.onclick = () => {
            // Scroll suau fins a la secció de felicitacions
            const congratsSection = document.querySelector('.bg-success.text-white.rounded');
            if (congratsSection) {
              congratsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          };
        } else {
          nextBtn.innerHTML = 'Següent<i class="fas fa-arrow-right ms-2"></i>';
          nextBtn.onclick = () => changeStep(1);
        }
      }
    }
    
    // Inicialitza el wizard
    showStep(1);
  }
});