# -*- coding: utf-8 -*-

# Good explanations of how French verb conjugation works:
#   http://fr.wiktionary.org/wiki/Annexe:Conjugaison_en_fran%C3%A7ais
#   http://www.french-linguistics.co.uk/grammar/irregular_verbs_paradigms.shtml

# Get our registry.
from conjugator import BY_LABEL, ALL

# Load each group of conjugators.
import irregular_conjugators
import er_conjugators
import ir_conjugators
import re_conjugators

# Register the verbs in our database with the appropriate conjugator.
def register_verbs_from_database(conn):
    # We sort by frequency because the first verb registered will become
    # the example verb.
    query = """
    SELECT prototype, lemme FROM verbe
    WHERE prototype IS NOT NULL
    ORDER BY freqfilms2 DESC"""
    for row in conn.execute(query):
        label, lemme = row
        conj = BY_LABEL[label]
        conj.register_verb(lemme)
