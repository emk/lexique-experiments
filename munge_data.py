# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import sqlite3
import prototype
import conjugators

# Open our database.
db = sqlite3.connect("lexique.sqlite3")

# Figure out what protype goes with each verb.
print("Determining verb prototypes...", file=sys.stderr)
verb_prototypes = []
for row in db.execute('SELECT lemme FROM verbe'):
    verb = row[0]
    for p in prototype.PROTOTYPES:
        if p.matches(verb):
            conj = conjugators.BY_LABEL[p.label]
            verb_prototypes.append((p.label, conj.name(), p.aux, verb))
            break

# Update all our our verb fields in one pass.
print("Storing verb prototypes...", file=sys.stderr)
sql = "UPDATE verbe SET prototype = ?, conjugator = ?, aux = ? WHERE lemme = ?"
db.executemany(sql, verb_prototypes)
db.commit()
