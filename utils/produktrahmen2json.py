#!/usr/bin/env python3

import re

from docx import Document
from docx.text.paragraph import Paragraph

# From https://github.com/stadt-karlsruhe/budget-export
def split(s, maxsplit=None):
    '''
    Split a string at whitespace.
    Works like ``str.split`` with no explicit separator, i.e. splits
    the string ``s`` at any whitespace. In contrast to ``str.split``,
    however, you can set the maximum number of splits via ``maxsplit``
    while not having to pass an explicit separator.
    '''
    return re.split(r'\s+', s.strip(), maxsplit=maxsplit, flags=re.UNICODE)


# Adapated from https://github.com/python-openxml/python-docx/issues/276
def get_paragraphs(parent):
    '''
    Generate a reference to each paragraph child within ``parent``, in
    document order. Each returned value is an instance of ``Paragraph``.
    ``parent`` would most commonly be a reference to a main ``Document``
    object, but also works for a ``_Cell`` object.
    '''
    from docx.document import Document as _Document
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.table import _Cell

    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError('Unknown parent class {}'.format(
                         parent.__class__.__name__))

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)

if __name__ == '__main__':
    import json
    import sys
    doc = Document(sys.argv[1])

    bereiche = {}
    bereich = None
    gruppe = None
    produkt = None
    current_object = None
    paragraphs = get_paragraphs(doc)
    for para in paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if text == 'Produktbereich:':
            next_para = next(paragraphs)
            number, title = split(next_para.text.strip(), 1)
            if not number.isdigit():
                # Special case
                number = '12'
                title = 'Sicherheit und Ordnung'
            current_object = bereich = bereiche[number] = {
                'titel': title,
                'nummer': number,
                'gruppen': {},
                'beschreibung': '',
                'ziele': '',
                'buchungshinweis': '',
                'rechnungslegungshinweis': '',
            }
            current_key = None
            gruppe = None
            produkt = None
        elif text == 'Produktgruppe:':
            next_para = next(paragraphs)
            fields = split(next_para.text.strip(), 1)
            if len(fields) < 2:
                # Special case
                    fields.insert(0, '11.23')
            number, title = fields
            current_object = gruppe = bereich['gruppen'][number] = {
                'titel': title,
                'nummer': number,
                'bereich': bereich['nummer'],
                'produkte': {},
                'beschreibung': '',
                'ziele': '',
                'buchungshinweis': '',
                'rechnungslegungshinweis': '',
            }
            current_key = None
            produkt = None
        elif text == 'Produkt:':
            next_para = next(paragraphs)
            number, title = split(next_para.text.strip(), 1)
            current_object = produkt = gruppe['produkte'][number] = {
                'titel': title,
                'nummer': number,
                'gruppe': gruppe['nummer'],
                'beschreibung': '',
                'ziele': '',
                'buchungshinweis': '',
                'rechnungslegungshinweis': '',
            }
            current_key = None
        elif text == 'Kurzbeschreibung:':
            current_key = 'beschreibung'
        elif text == 'Allgemeine Ziele / Auftragsgrundlage:':
            current_key = 'ziele'
        elif text in ['Buchungshinweis:', 'Buchungshinweise:']:
            current_key = 'buchungshinweis'
        elif text in ['Rechnungslegungshinweis:', 'Rechnungslegungshinweise:']:
            current_key = 'rechnungslegungshinweis'
        else:
            key = current_key or 'beschreibung'
            current_object[key] = (current_object[key] + '\n' + text).strip()

    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(bereiche, f)

