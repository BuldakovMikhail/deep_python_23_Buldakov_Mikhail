import json


def parse_json(
    json_str: str, keyword_callback, required_fields=None, keywords=None
) -> None:
    """
    Функция, которая в качестве аргументов принимает строку json, список полей, которые необходимо обработать, список имён, которые нужно найти и функцию-обработчика имени, который срабатывает, когда в каком-либо поле было найдено ключевое имя. Если аргумент required_fields не задан, функция-обработчик вызывается для всех полей, в которых есть keywords. Если аргумент keywords не задан, функция-обработчик вызывается для всех слов полей required_fields.
    """

    if keyword_callback is None:
        raise ValueError("Callback function must be not None")

    json_doc = json.loads(json_str)

    if required_fields is None:
        required_fields = list(json_doc.keys())

    for rf in required_fields:
        if rf in json_doc.keys():
            value = json_doc[rf]
            values = value.split()

            if keywords is None:
                for v in values:
                    keyword_callback(rf, v)
            else:
                keys = list(map(lambda x: x.lower(), value.split()))

                for kw in keywords:
                    calls_count = keys.count(kw.lower())
                    for _ in range(calls_count):
                        keyword_callback(rf, kw)
