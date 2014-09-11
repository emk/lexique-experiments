# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import codecs

import sqlite3

import prototype
import conjugators

# Python 2.7 is really unbearably stupid about Unicode.  Here is one of the
# bigger patches we need to make: http://stackoverflow.com/questions/492483/
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# Open our database.
db = sqlite3.connect("lexique.sqlite3")

# Order our prototypes by coverage.
prototypes = []
query = """
SELECT prototype FROM verbe
  WHERE prototype IS NOT NULL
  GROUP BY prototype
  ORDER BY SUM(freqfilms2) DESC"""
for row in db.execute(query):
    prototypes.append(prototype.BY_LABEL[row[0]])

# For each conjugator, use the highest-frequency verb as an example.
query = """
SELECT prototype, lemme FROM verbe
  WHERE prototype IS NOT NULL
  ORDER BY freqfilms2 DESC"""
for row in db.execute(query):
    label, lemme = row
    conj = conjugators.BY_LABEL[label]
    conj.register_verb(lemme)

for conj in conjugators.ALL:
    print("%s: %s" % (conj.name(), conj.summarize()))

# Iterate over our prototypes until we hit a mismatch.
for p in prototypes:
    conj = conjugators.BY_LABEL[p.label]
    conj.assert_matches_prototype(p)
