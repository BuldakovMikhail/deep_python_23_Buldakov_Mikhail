# Есть текстовый файл, который может не помещаться в память. В каждой строке файла фраза или предложение: набор слов, разделенных пробелами (знаков препинания нет).

# Генератор должен принимать на вход имя файла или файловый объект и список слов для поиска. Генератор перебирает строки файла и возвращает только те из них (строку целиком), где встретилось хотя бы одно из слов для поиска. Поиск должен выполняться по полному совпадению слова без учета регистра.

# Например, для строки из файла "а Роза упала на лапу Азора" слово поиска "роза" должно найтись, а "роз" или "розан" - уже нет.


def __searcher(input_file, search_words_lc):
    while (x := input_file.readline()):
        x = x.strip()
        words = list(map(str.lower, x.split(' ')))
        flag = False
        for sw in search_words_lc:
            if sw in words:
                flag = True
                break
        if flag:
            yield x


def gen_selected_lines(file_name, search_words):
    if not search_words:
        raise Exception('No words for search have been passed')

    lower_cased_sw = list(map(str.lower, search_words))

    if isinstance(file_name, str):
        with open(file_name, mode='r') as src:
            yield from __searcher(src, lower_cased_sw)
    elif hasattr(file_name, "readline"):
        yield from __searcher(file_name, lower_cased_sw)
    else:
        raise Exception('Neither file or file object')
