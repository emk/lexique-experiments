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

