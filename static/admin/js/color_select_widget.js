// JavaScript per millorar ColorSelectWidget
document.addEventListener('DOMContentLoaded', function() {
    
    // Afegir previsualització del color seleccionat
    function addColorPreview() {
        const colorSelects = document.querySelectorAll('.field-color select');
        
        colorSelects.forEach(function(select) {
            // Crear element de previsualització
            const preview = document.createElement('span');
            preview.className = 'color-preview';
            
            // Inserir després del select
            select.parentNode.insertBefore(preview, select.nextSibling);
            
            // Funció per actualitzar la previsualització
            function updatePreview() {
                const selectedValue = select.value;
                if (selectedValue && selectedValue.startsWith('#')) {
                    preview.style.backgroundColor = selectedValue;
                    preview.style.display = 'inline-block';
                } else {
                    preview.style.display = 'none';
                }
            }
            
            // Actualitzar quan canvia la selecció
            select.addEventListener('change', updatePreview);
            
            // Actualitzar al carregar la pàgina
            updatePreview();
        });
    }
    
    // Executar quan es carrega la pàgina
    addColorPreview();
    
    // També executar quan Django inline forms s'afegeixen dinàmicament
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function() {
            setTimeout(addColorPreview, 100);
        });
    }
});