#!/usr/bin/env python3

import csv
import re
import sys


def clean_number(s):
    return re.sub(r'\D', '', str(s))

def clean_description(s):
    return re.sub(r' +', ' ', s)

def convert(reader):
    # Skip header
    next(reader)

    klassen = {}
    for row in reader:
        description = clean_description(row[6])
        if row[0]:
            number = clean_number(row[0])
            klasse = klassen[number] = {
                'bezeichnung': description,
                'bereichsabgrenzung': row[5],
                'gruppen': {},
            }
        elif row[1]:
            number = clean_number(row[1])
            gruppe = klasse['gruppen'][number] = {
                'bezeichnung': description,
                'bereichsabgrenzung': row[5],
                'arten': {},
            }
        elif row[2]:
            number = clean_number(row[2])
            art = gruppe['arten'][number] = {
                'bezeichnung': description,
                'bereichsabgrenzung': row[5],
                'konten': {},
            }
        elif row[3]:
            number = clean_number(row[3])
            konto = art['konten'][number] = {
                'bezeichnung': description,
                'bereichsabgrenzung': row[5],
                'unterkonten': {},
            }
        elif row[4]:
            number = clean_number(row[4])
            unterkonto = konto['unterkonten'][number] = {
                'bezeichnung': description,
                'bereichsabgrenzung': row[5],
            }
        elif any(row):
            sys.stderr.write("Dont' know what to do with {}\n".format(row))

    return klassen


if __name__ == '__main__':
    import json
    with open(sys.argv[1], 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, dialect='unix')
        data = convert(reader)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(data, f)

