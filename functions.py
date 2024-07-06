from urllib.parse import urlparse

from minio_client import MINIO_BUCKET_NAME


async def translit(text):
    """
    Переводит текст в транслит.

    Аргументы:
    text (str): Текст, который требуется перевести в транслит.

    Возвращает:
    str: Текст, переведенный в транслит.

    Примеры:
    >>> translit('Привет, мир!')
    'Privet, mir!'
    >>> translit('Это пример текста для транслитерации.')
    'Eto primer teksta dlya transliteratsii.'
    """
    trans_table = str.maketrans(
        {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
         'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
         'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y',
         'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', })
    return text.lower().translate(trans_table)


async def extract_relative_path(url: str) -> str:
    """
    Извлекает относительную часть пути из URL,
    исключая указанный базовый сегмент.

    Аргументы:
        url (str): Строка URL.
        base_segment (str): Базовый сегмент,
        который нужно исключить из результата.

    Возвращает:
        str: Относительная часть пути из URL,
        исключая указанный базовый сегмент.

    Пример использования:
        >>> url = 'http://some_url/some_base_segment/1de9b97f87f0--strelka.png'
        >>> relative_path = extract_relative_path(url, '/memes/')
        >>> print(relative_path)
        '1de9b97f87f0--strelka.png'
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    base_index = path.find(f'/{MINIO_BUCKET_NAME}/')

    if base_index != -1:
        relative_path = path[base_index + len(f'/{MINIO_BUCKET_NAME}/'):]
    else:
        # Если base_segment не нашли, возвращаем весь путь
        relative_path = path

    return relative_path
