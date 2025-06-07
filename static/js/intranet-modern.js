/**
 * Civada - Funcionalidades modernas para la intranet
 */

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // Inicializar popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  if (popoverTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
    popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  }

  // Animación para las tarjetas
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.classList.add('animate__animated', 'animate__fadeIn');
  });

  // Animación para las small-boxes
  const smallBoxes = document.querySelectorAll('.small-box');
  smallBoxes.forEach((box, index) => {
    box.style.animationDelay = `${index * 0.1}s`;
    box.classList.add('animate__animated', 'animate__fadeInUp');
  });

  // Mejorar la interacción con las tablas
  const tables = document.querySelectorAll('.table');
  tables.forEach(table => {
    if (!table.classList.contains('table-hover')) {
      table.classList.add('table-hover');
    }
  });

  // Añadir efecto de ondas a los botones (estilo Material Design)
  function createRipple(event) {
    const button = event.currentTarget;
    
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
    circle.classList.add('ripple');
    
    const ripple = button.getElementsByClassName('ripple')[0];
    
    if (ripple) {
      ripple.remove();
    }
    
    button.appendChild(circle);
  }
  
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(button => {
    button.addEventListener('click', createRipple);
  });

  // Mejorar la navegación del sidebar
  const navLinks = document.querySelectorAll('.nav-sidebar .nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      if (this.nextElementSibling && this.nextElementSibling.classList.contains('nav-treeview')) {
        e.preventDefault();
        const parent = this.parentElement;
        if (parent.classList.contains('menu-open')) {
          parent.classList.remove('menu-open');
          this.nextElementSibling.style.display = 'none';
        } else {
          parent.classList.add('menu-open');
          this.nextElementSibling.style.display = 'block';
        }
      }
    });
  });

  // Botón para alternar la visibilidad del sidebar
  const sidebarToggleBtn = document.querySelector('[data-widget="pushmenu"]');
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', function(e) {
      e.preventDefault();
      document.body.classList.toggle('sidebar-collapse');
      
      // Guardar preferencia en localStorage
      const sidebarCollapsed = document.body.classList.contains('sidebar-collapse');
      localStorage.setItem('sidebar-collapsed', sidebarCollapsed);
    });
    
    // Restaurar estado del sidebar desde localStorage
    const sidebarCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (sidebarCollapsed) {
      document.body.classList.add('sidebar-collapse');
    }
  }

  // Añadir contador de notificaciones
  function updateNotificationCount() {
    const notificationBadge = document.querySelector('.notification-badge');
    if (notificationBadge) {
      // Aquí se podría hacer una petición AJAX para obtener el número real de notificaciones
      const count = Math.floor(Math.random() * 10); // Simulación
      notificationBadge.textContent = count;
      notificationBadge.style.display = count > 0 ? 'inline-block' : 'none';
    }
  }
  
  // Actualizar cada 5 minutos (simulación)
  updateNotificationCount();
  setInterval(updateNotificationCount, 300000);

  // Mejorar la visualización de datos en tablas largas
  const dataTables = document.querySelectorAll('.datatable');
  if (dataTables.length > 0 && typeof $.fn.DataTable !== 'undefined') {
    dataTables.forEach(table => {
      $(table).DataTable({
        "responsive": true,
        "autoWidth": false,
        "language": {
          "url": "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
        }
      });
    });
  }

  // Añadir funcionalidad de búsqueda en tiempo real
  const searchInputs = document.querySelectorAll('.search-input');
  searchInputs.forEach(input => {
    input.addEventListener('keyup', function() {
      const searchTerm = this.value.toLowerCase();
      const targetId = this.dataset.target;
      const targetItems = document.querySelectorAll(`#${targetId} .search-item`);
      
      targetItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // Añadir efecto de carga para acciones que requieren tiempo
  const loadingButtons = document.querySelectorAll('.btn-loading');
  loadingButtons.forEach(button => {
    button.addEventListener('click', function() {
      const originalText = this.innerHTML;
      this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
      this.disabled = true;
      
      // Restaurar después de un tiempo (simulación)
      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
      }, 2000);
    });
  });

  // Mejorar la visualización de gráficos si existen
  const chartElements = document.querySelectorAll('.chart');
  if (chartElements.length > 0 && typeof Chart !== 'undefined') {
    chartElements.forEach(element => {
      // Aquí se podría inicializar Chart.js con datos específicos
      // Este es solo un ejemplo genérico
      const ctx = element.getContext('2d');
      new Chart(ctx, {
        type: element.dataset.type || 'bar',
        data: {
          labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
          datasets: [{
            label: element.dataset.label || 'Datos',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              'rgba(46, 125, 50, 0.2)',
              'rgba(46, 125, 50, 0.4)',
              'rgba(46, 125, 50, 0.6)',
              'rgba(46, 125, 50, 0.8)',
              'rgba(46, 125, 50, 1)',
              'rgba(255, 143, 0, 0.8)'
            ],
            borderColor: [
              'rgba(46, 125, 50, 1)',
              'rgba(46, 125, 50, 1)',
              'rgba(46, 125, 50, 1)',
              'rgba(46, 125, 50, 1)',
              'rgba(46, 125, 50, 1)',
              'rgba(255, 143, 0, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    });
  }
});

// Añadir estilos para el efecto de ondas
document.head.insertAdjacentHTML('beforeend', `
  <style>
    .ripple {
      position: absolute;
      background-color: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s linear;
      pointer-events: none;
    }

    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
    
    .btn {
      position: relative;
      overflow: hidden;
    }
  </style>
`);