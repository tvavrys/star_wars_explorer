from django import template
from django.http import QueryDict
from django.shortcuts import reverse

register = template.Library()


@register.inclusion_tag("explorer/tags.html", takes_context=True)
def group_by_tags(context, tags):
    """TODO"""
    params = context["request"].GET.copy()
    active_columns = params.getlist("columns", [])

    _tags = []
    for tag in tags:
        base_url = reverse("collection-group-by-view", args=[context["object"].pk])
        is_active = tag in active_columns

        tag_params = QueryDict(mutable=True)
        if not is_active:
            tag_params.setlist("columns", active_columns + [tag])
        else:
            columns = active_columns[:]
            columns.remove(tag)
            tag_params.setlist("columns", columns)

        url = f"{base_url}?{tag_params.urlencode()}"
        _tags.append(
            {
                "title": tag,
                "url": url,
                "is_active": is_active,
            }
        )

    return {
        "tags": _tags,
    }
