from django import template

register = template.Library()

@register.filter
def primer_nombre(nombre_completo):
    if not isinstance(nombre_completo, str):
        return ''
    return nombre_completo.split(' ')[0]