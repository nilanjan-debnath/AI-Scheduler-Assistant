from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def toggle(context, var_name):
    context[var_name] = not context.get(var_name, True)
    return ''

