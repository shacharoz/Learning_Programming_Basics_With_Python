import json

from jinja2.utils import htmlsafe_json_dumps as html_sanitize
from jinja2 import evalcontextfilter


def json_dumps_default(obj):
    if hasattr(obj, 'tojson'):
        return obj.tojson()
    else:
        raise TypeError(f'Object of type {o.__class__.__name__} ' +
                        f'is not JSON serializable')


json_dumps_kwargs = {
    'skipkeys': False,
    'ensure_ascii': True,
    'check_circular': True,
    'allow_nan': True,
    'sort_keys': True,
    'indent': None,
    'separators': (',', ':'),
    'default': json_dumps_default,
}


def json_dumps(obj, **kwargs):
    options = json_dumps_kwargs
    if kwargs:
        for key, value in kwargs.items():
            options[key] = value
    return json.dumps(obj, **options)


@evalcontextfilter
def do_tojson(ctx, obj, **kwargs):
    return html_sanitize(obj, dumper=json_dumps, **kwargs)
