import yaml
from jinja2 import Template

with open("strings.yml", encoding='utf-8') as file:
    strings = yaml.safe_load(file)


def get_text(lang: str, key: str, **kwargs) -> str:
    raw_template = strings.get(lang, {}).get(key, "")
    return Template(raw_template).render(**kwargs)
