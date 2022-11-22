from django import template
from datetime import datetime
import json

register = template.Library()


@register.filter
def to_date(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


@register.filter
def json_encode(value):
    return json.dumps(value)
