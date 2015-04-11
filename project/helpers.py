import re


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+').split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))
