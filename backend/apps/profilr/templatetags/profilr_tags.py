import json
from datetime import datetime

from django import template

register = template.Library()


@register.filter
def to_date(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


@register.filter
def json_encode(value):
    return json.dumps(value)
