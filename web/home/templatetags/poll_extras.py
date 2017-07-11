from django import template

register = template.Library()

@register.filter
def trim(value):
    return str(value).replace(" ", "")

@register.filter
def replace_blank_get(value):
    value = value.replace("%","%25")
    value = value.replace("#", "%23")
    value = value.replace("{", "%7B")
    value = value.replace("}", "%7D")
    value = value.replace("|", "%7C")
    value = value.replace("\\", "%5C")
    value = value.replace("^", "%5E")
    value = value.replace("~", "%7E")
    value = value.replace("[", "%5B")
    value = value.replace("]", "%5D")
    value = value.replace("`", "%60")
    value = value.replace(";", "%3B")
    value = value.replace("/", "%2F")
    value = value.replace("?", "%3F")
    value = value.replace(":", "%3A")
    value = value.replace("@", "%40")
    value = value.replace("=", "%3D")
    value = value.replace("&", "%26")
    value = value.replace("$", "%24")
    return value