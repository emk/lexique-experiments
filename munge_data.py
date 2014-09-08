# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import sqlite3
import prototype

# Open our database.
db = sqlite3.connect("lexique.sqlite3")

# Figure out what protype goes with each verb.
print("Determining verb prototypes...", file=sys.stderr)
verb_prototypes = []
for row in db.execute('SELECT lemme FROM verbe'):
    verb = row[0]
    for p in prototype.PROTOTYPES:
        if p.matches(verb):
            verb_prototypes.append((p.label, p.aux, verb))
            break

# Update all our our verb fields in one pass.
print("Storing verb prototypes...", file=sys.stderr)
db.executemany("UPDATE verbe SET prototype = ?, aux = ? WHERE lemme = ?",
               verb_prototypes)
db.commit()
