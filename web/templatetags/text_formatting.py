from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def smart_format(value):
    """
    Converteix text pla en HTML formatat automàticament:
    - Lines que comencen amb "• " o "- " → <li>
    - Dobles salts de línia → paràgrafs separats
    - Manté enllaços HTML existents
    """
    if not value:
        return ""
    
    # Dividir per dobles salts de línia per fer paràgrafs
    paragraphs = re.split(r'\n\s*\n', value.strip())
    
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        # Detectar si és una llista (lines que comencen amb • o -)
        lines = paragraph.split('\n')
        
        # Comprovar si la majoria de línies són items de llista
        list_items = []
        regular_text = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('• ') or line.startswith('- '):
                # Eliminar el símbol i netejar
                item_text = line[2:].strip()
                list_items.append(f'<li>{item_text}</li>')
            elif line:
                regular_text.append(line)
        
        if list_items and not regular_text:
            # És una llista pura
            formatted_paragraphs.append(f'<ul class="list-formatted">{" ".join(list_items)}</ul>')
        elif list_items and regular_text:
            # Text mixt: primer el text regular, després la llista
            regular_html = '<p>' + ' '.join(regular_text) + '</p>'
            list_html = f'<ul class="list-formatted">{" ".join(list_items)}</ul>'
            formatted_paragraphs.append(regular_html + list_html)
        else:
            # Text normal sense llistes
            if paragraph.strip():
                formatted_paragraphs.append(f'<p>{paragraph.strip()}</p>')
    
    return mark_safe('\n'.join(formatted_paragraphs))

@register.filter
def smart_format_comissions(value):
    """
    Format específic per al text de comissions amb títols en negreta
    """
    if not value:
        return ""
    
    # Dividir per dobles salts de línia
    sections = re.split(r'\n\s*\n', value.strip())
    
    formatted_sections = []
    
    for section in sections:
        section = section.strip()
        if ':' in section:
            # Detectar patró "Títol: descripció"
            parts = section.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                formatted_sections.append(f'<div class="commission-item mb-2"><strong>{title}:</strong> {description}</div>')
            else:
                formatted_sections.append(f'<p>{section}</p>')
        else:
            formatted_sections.append(f'<p>{section}</p>')
    
    return mark_safe(''.join(formatted_sections))