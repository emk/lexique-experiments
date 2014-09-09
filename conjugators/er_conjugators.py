# -*- coding: utf-8 -*-

import re
from conjugator import *

@conjugates([u'.*er', u'arriver|entrer|rentrer|rester|retomber|tomber',
             u'.*ger', u'.*cer'])
class ErConjugator(Conjugator):
    REMOVE = 'er'
    PAST_PARTICIPLE = u'é'
    SINGULAR_RADICAL = 'e'
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''
    FUTURE_RADICAL = 'er'
    # We put the 'a' into our endings, because of 'èrent'.
    SIMPLE_PAST_RADICAL = ''

    PRESENT_SUFFIXES = ['', 's', '', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['', 'ons', 'ez']
    SIMPLE_PAST_SUFFIXES = ['ai', 'as', 'a', u'âmes', u'âtes', u'èrent']
    SUBJUNCTIVE_IMPERFECT_SUFFIXES = \
      ['asse', 'asses', u'ât', 'assions', 'assiez', 'assent']

@conjugates([u'.*e([lt])er'])
class ElerConjugator(ErConjugator):
    REMOVE = '([lt])er'
    SINGULAR_RADICAL = '\\1\\1e'
    TONIC_RADICAL = '\\1\\1'
    FUTURE_RADICAL = '\\1\\1er'

# Non-doubling version of the rule above.
@conjugates([u'acheter|bégueter|bouveter|breveter|caleter|corseter|crocheter|émoucheter|fileter|fureter|haleter|préacheter|racheter|.*éceter', u'aciseler|celer|ciseler|congeler|crêpeler|déceler|décongeler|dégeler|démanteler|écarteler|embreler|encasteler|épinceler|friseler|geler|harceler|marteler|modeler|peler|receler|recongeler|regeler|remodeler|surgeler'])
class EterConjugator(ErConjugator):
    REMOVE = 'e([lt])er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'
    FUTURE_RADICAL = u'è\\1er'

# TODO: Why are -éger verbs broken out in the XML dataset?
@conjugates([u'.*é([djlmnprsty])er', u'.*éger', u'.*ég([lnru])er', u'.*écher',
             u'.*é([bctv])rer'])
class ErerConjugator(ErConjugator):
    REMOVE = u'é([djlmnprsty]|g|g[lnru]|ch|[bctv]r)er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'

@conjugates([u'.*e([mnprsv])er'])
class EmerConjugator(ErConjugator):
    REMOVE = 'e([mnprsv])er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'
    FUTURE_RADICAL = u'è\\1er'

@conjugates([u'.*oyer|.*uyer'])
class YerConjugator(ErConjugator):
    REMOVE = 'yer'
    SINGULAR_RADICAL = 'ie'
    TONIC_RADICAL = 'i'
    FUTURE_RADICAL = 'ier'

@conjugates([u'.*ayer'])
class AyerConjugator(YerConjugator):
    REMOVE = 'yer'
    SINGULAR_RADICAL = 'ie|ye'
    TONIC_RADICAL = 'i|y'
    FUTURE_RADICAL = 'ier|yer'

@conjugates([u'envoyer|renvoyer'])
class VoyerConjugator(YerConjugator):
    REMOVE = 'oyer'
    FUTURE_RADICAL = 'err'

@conjugates([u'ficher'])
class FicherConjugator(ErConjugator):
    REMOVE = 'er'
    PAST_PARTICIPLE = u'é|u' # By analogy to foutu.

