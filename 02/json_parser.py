import json


def parse_json(
    json_str: str, keyword_callback, required_fields=None, keywords=None
) -> None:
    """
    Функция, которая в качестве аргументов принимает строку json, список полей, которые необходимо обработать, список имён, которые нужно найти и функцию-обработчика имени, который срабатывает, когда в каком-либо поле было найдено ключевое имя. Если аргумент required_fields задан, функция-обработчик вызывается для всех полей, в которых есть keywords. Если аргумент keywords не задан, функция-обработчик вызывается для всех слов полей required_fields.
    """

    json_doc = json.loads(json_str)

    if required_fields is None:
        required_fields = list(json_doc.keys())

    for rf in required_fields:
        if rf in json_doc.keys():
            value = json_doc[rf]
            values = value.split(" ")

            if keywords is None:
                for v in values:
                    keyword_callback(v)
            else:
                keys = list(map(lambda x: x.lower(), value.split(" ")))
                values_dict = dict(
                    zip(keys, values)
                )  # Создаем словар, где ключ - форматированное слово, а значение - исходное

                for k in keywords:
                    if k.lower() in values_dict.keys():
                        keyword_callback(values_dict[k.lower()])
