import html

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
