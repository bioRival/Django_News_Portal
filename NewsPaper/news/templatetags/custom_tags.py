from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()


@register.filter('in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()