# -*- coding: utf-8 -*-

# See http://french.about.com/od/grammar/a/erverbs_irreg.htm

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

# Consonant doubling in some forms.  Historically, there have been a large
# number of verbs in this category, but the Rectifications orthographiques
# du français in 1990 move all of them to the peler/acheter category below,
# with the exception of appeler, jeter, and their derivatives, which retain
# their traditional forms.
@conjugates([u'.*e([lt])er'])
class ElerConjugator(ErConjugator):
    REMOVE = '([lt])er'
    SINGULAR_RADICAL = '\\1\\1e'
    TONIC_RADICAL = '\\1\\1'
    FUTURE_RADICAL = '\\1\\1er'

# Transforming e -> è.  Future tense included.
@conjugates([u'acheter|bégueter|bouveter|breveter|caleter|corseter|crocheter|émoucheter|fileter|fureter|haleter|préacheter|racheter|.*éceter', u'aciseler|celer|ciseler|congeler|crêpeler|déceler|décongeler|dégeler|démanteler|écarteler|embreler|encasteler|épinceler|friseler|geler|harceler|marteler|modeler|peler|receler|recongeler|regeler|remodeler|surgeler', u'.*e([mnprsv])er'])
class EterConjugator(ErConjugator):
    REMOVE = 'e([lt]|[mnprsv])er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'
    FUTURE_RADICAL = u'è\\1er'

# Transforming é -> è.  Future tense not included.
# TODO: Why are -éger verbs broken out in the XML dataset?
@conjugates([u'.*é([djlmnprsty])er', u'.*éger', u'.*ég([lnru])er', u'.*écher',
             u'.*é([bctv])rer'])
class ErerConjugator(ErConjugator):
    REMOVE = u'é([djlmnprsty]|g|g[lnru]|ch|[bctv]r)er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'

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
