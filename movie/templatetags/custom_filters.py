from django import template


register = template.Library()


@register.filter(name='duration_format')
def duration_format(value):
    try:
        minutes = int(value)
    except (ValueError, TypeError):
        return

    if minutes <= 0:
        return

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours > 0 and remaining_minutes > 0:
        return f"{hours} ساعت {remaining_minutes} دقیقه"
    elif hours > 0:
        return f"{hours} ساعت"
    else:
        return f"{minutes} دقیقه"


@register.filter
def classname(obj):
    return obj.__class__.__name__
