# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import re
import xml.etree.ElementTree as ET
import sqlite3

# A verb prototype.  Loaded from XML.
class Prototype:
    def __init__(self, element):
        regex = element.get('REGEX')
        self.label = regex.replace("(?'c'", "(")
        new_regex = "(?:%s)$" % regex.replace("(?'c'", "(?P<c>")
        self.regex = re.compile(new_regex)
        self.infinitive = element.get('INFINITIVE')
        self.notes = element.get('NOTES')
        self.radical = element.get('RADICAL')
        self.ending = element.get('ENDING')
        self.aux = element.get('AUX')
        self.ppresent = element.get('PPRESENT')
        self.ppasse = element.get(u'PPASSÉ')
        self.present = element.get(u'PRÉSENT')
        self.imparfait = element.get('IMPARFAIT')
        self.futur = element.get('FUTUR')
        self.simparfait = element.get('SIMPARFAIT')
        self.imperatif = element.get(u'IMPÉRATIF')
        self.condition = element.get('CONDITION')

    def matches(self, infinitive):
        return self.regex.match(infinitive)

# Load our verb prototypes from XML.
conjugator = ET.parse('verbs-0-2-0.xml').getroot()
prototypes = [Prototype(p) for p in conjugator.findall('Prototype')]

# Open our database.
db = sqlite3.connect("lexique.sqlite3")

# Figure out what protype goes with each verb.
print("Determining verb prototypes...", file=sys.stderr)
verb_prototypes = []
for row in db.execute('SELECT lemme FROM verbe'):
    verb = row[0]
    for p in prototypes:
        if p.matches(verb):
            verb_prototypes.append((p.label, verb))
            break

# Update all our our verb fields in one pass.
print("Storing verb prototypes...", file=sys.stderr)
db.executemany("UPDATE verbe SET prototype = ? WHERE lemme = ?", verb_prototypes)
db.commit()
