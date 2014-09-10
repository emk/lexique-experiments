# -*- coding: utf-8 -*-

from __future__ import print_function
import sqlite3
import prototype

import conjugators

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
    if conj.example_verb is None:
        conj.example_verb = lemme

for conj in conjugators.ALL:
    print("====", conj.name())
    print(conj.summarize_forms())

# Iterate over our prototypes until we hit a mismatch.
for p in prototypes:
    conj = conjugators.BY_LABEL[p.label]
    conj.assert_matches_prototype(p)
