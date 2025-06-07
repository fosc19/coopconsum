function igualarAlturaBloquesProductos() {
  // Selecciona todos los bloques de la galería
  const cards = document.querySelectorAll('.producto-card');
  if (!cards.length) return;

  // Bloques internos a igualar
  const titulos = Array.from(document.querySelectorAll('.producto-titulo'));
  const descripciones = Array.from(document.querySelectorAll('.producto-descripcion'));
  const precios = Array.from(document.querySelectorAll('.producto-precio'));

  // Resetear alturas
  titulos.forEach(e => e.style.height = 'auto');
  descripciones.forEach(e => e.style.height = 'auto');
  precios.forEach(e => e.style.height = 'auto');

  // Calcular máximos
  const maxTitulo = Math.max(...titulos.map(e => e.offsetHeight));
  const maxDescripcion = Math.max(...descripciones.map(e => e.offsetHeight));
  const maxPrecio = Math.max(...precios.map(e => e.offsetHeight));

  // Aplicar máximos
  titulos.forEach(e => e.style.height = maxTitulo + 'px');
  descripciones.forEach(e => e.style.height = maxDescripcion + 'px');
  precios.forEach(e => e.style.height = maxPrecio + 'px');
}

// Ejecutar al cargar y al redimensionar
window.addEventListener('load', igualarAlturaBloquesProductos);
window.addEventListener('resize', igualarAlturaBloquesProductos);