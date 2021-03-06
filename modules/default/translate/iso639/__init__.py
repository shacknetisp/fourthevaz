import os
import codecs


class NonExistentLanguageError(RuntimeError):
    pass


def find(whatever=None, language=None, iso639_1=None, iso639_2=None):
    if whatever:
        keys = ['name', 'iso639_1', 'iso639_2_b', 'iso639_2_t']
        val = whatever
    elif language:
        keys = ['name']
        val = language
    elif iso639_1:
        keys = ['iso639_1']
        val = iso639_1
    elif iso639_2:
        keys = ['iso639_2_b', 'iso639_2_t']
        val = iso639_2
    else:
        raise ValueError('Invalid search criteria.')
    val = str(val)
    return next((item for item in data if any(
        item[key].lower() == val.lower() for key in keys)), None)


def is_valid639_1(code):
    if len(code) != 2:
        return False
    return find(iso639_1=code) is not None


def is_valid639_2(code):
    if len(code) != 3:
        return False
    return find(iso639_2=code) is not None


def to_iso639_1(key):
    item = find(whatever=key)
    if not item:
        raise NonExistentLanguageError('Language does not exist.')
    return item['iso639_1']


def to_iso639_2(key, type='B'):
    if not type in ('B', 'T'):
        raise ValueError('Type must be either "B" or "T".')
    item = find(whatever=key)
    if not item:
        raise NonExistentLanguageError('Language does not exist.')
    if type == 'T' and item['iso639_2_t']:
        return item['iso639_2_t']
    return item['iso639_2_b']


def to_name(key):
    item = find(whatever=key)
    if not item:
        raise NonExistentLanguageError('Language does not exist.')
    return item['name']


def _load_data():
    def parse_line(line):
        data = line.strip().split('|')
        return {
            'iso639_2_b': data[0],
            'iso639_2_t': data[1],
            'iso639_1': data[2],
            'name': data[3].split(';')[0],
        }

    data_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'ISO-639-2_utf-8.txt')
    with codecs.open(data_file, 'r', 'UTF-8') as f:
        data = [parse_line(line) for line in f]
    return data

data = _load_data()

