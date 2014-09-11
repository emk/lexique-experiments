# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import sqlite3
import prototype
import conjugators

# Open our database.
conn = sqlite3.connect("lexique.sqlite3")

# Figure out what prototype goes with each verb.
print("Determining verb prototypes...", file=sys.stderr)
verb_prototypes = []
for row in conn.execute('SELECT lemme FROM verbe'):
    verb = row[0]
    for p in prototype.PROTOTYPES:
        if p.matches(verb):
            verb_prototypes.append((p.label, p.aux, verb))
            break
sql = "UPDATE verbe SET prototype = ?, aux = ? WHERE lemme = ?"
conn.executemany(sql, verb_prototypes)

# Give nice names to our conjugators.
print("Determining verb conjugators...", file=sys.stderr)
conjugators.register_verbs_from_database(conn)
conn.executemany("INSERT INTO conjugaison VALUES (?, ?, ?)",
                 [(c.name(), c.like(), c.summarize()) for c in conjugators.ALL])

# Figure out what conjugator goes with each verb.
print("Matching conjugators to verbs...", file=sys.stderr)
verb_conjugators = []
for row in conn.execute('SELECT DISTINCT prototype FROM verbe'):
    label = row[0]
    verb_conjugators.append((conjugators.BY_LABEL[label].name(), label))
conn.executemany('UPDATE verbe SET conjugaison = ? WHERE prototype = ?',
                 verb_conjugators)

# Commit our changes.
conn.commit()
