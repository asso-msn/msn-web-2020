import html
from typing import Type

def linkify(link: str, class_="value", **kwargs):
    kwargs['href'] = kwargs.get('href', link)
    kwargs['class'] = class_
    return '<a {}>{}</a>'.format(
        ' '.join([f'{key}="{value}"' for key, value in kwargs.items()]),
        link,
    )

def handle_social(service, value):
    value = html.escape(value)
    special_cases = {
        'twitter': lambda x: linkify(f'@{x}', href=f'https://twitter.com/{x}')
    }
    if service in special_cases:
        return special_cases[service](value)
    return f'<span class="value">{value}</span>'

def handle_socials(d: dict):
    """Renders HTML for a dict of social in the form {"social_site": "value"}"""
    return [
        '<div class="social {}">{}</div>'.format(
            key,
            f'<span class="icon {key}"></span> ' + handle_social(key, value)
        ) for key, value in d.items()
    ]

def get_input(obj, field: str):
    type = getattr(obj.__class__, field).type.python_type
    value = getattr(obj, field)
    if type == bool:
        return '<select id="{field}" name="{field}">{options}</select>'.format(
            field=field,
            options=''.join([
                f'<option {"selected" if value == x else ""}>{int(x)}</option>'
                for x in [True, False]
            ])
        )
    if type == dict:
        return f'<textarea id="{field}" name="{field}">{value}</textarea>'
    return f'<input id="{field}" name="{field}" value={html.escape(value) if value else ""}>'

def get_inputs(obj, fields: list):
    return {
        field: get_input(obj, field)
        for field in fields
    }

