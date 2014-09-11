# -*- coding: utf-8 -*-

# See http://french.about.com/od/grammar/a/irverbs_irregular.htm

import re
from conjugator import *

# The regular verbs in this group insert an 'ss' in two radicals.  This is
# actually a superclass of the IrConjugator because that simplifies the
# rules.
@conjugates([u'.*ir'])
class IssConjugator(Conjugator):
    NAME = '-ir (-iss-)'

    REMOVE = 'r'
    PAST_PARTICIPLE = ''
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = 'ss'
    TONIC_RADICAL = 'ss'
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = ''

@conjugates([u'bénir'])
class BenirConjugator(IssConjugator):
    REMOVE = 'r'
    PAST_PARTICIPLE = '|t'

@conjugates([u'.*haïr'])
class HairConjugator(IssConjugator):
    REMOVE = u'ïr'
    SINGULAR_RADICAL = 'i'

    # The usual endings, but without the combining circumflex.
    SIMPLE_PAST_SUFFIXES = ['s', 's', 't', u'mes', u'tes', u'rent']
    SUBJUNCTIVE_IMPERFECT_SUFFIXES = \
      ['sse', 'sses', u't', 'ssions', 'ssiez', 'ssent']

# This is a version of the standard -ir conjugation, but without the '-iss'
# inserted in the tonic and atonic radicals.  All these verbs are actually
# irregular in some small way.
class IrConjugator(IssConjugator):
    NAME = '-ir'

    REMOVE = 'ir'
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''

@conjugates([u'partir', u'sortir', u'ressortir|.*mentir|.*sentir|.*partir',
             u'.*dormir', u'.*servir', 'mentir', '.*endormir|redormir'])
class TirConjugator(IrConjugator):
    REMOVE = '[tmv]ir'
    SINGULAR_RADICAL = ''

@conjugates([u'.*voir|.*oir'])
class VoirConjugator(IrConjugator):
    REMOVE = 'oir'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = 'oy'
    TONIC_RADICAL = 'oi'
    FUTURE_RADICAL = 'err'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'prévoir'])
class PrevoirConjugator(VoirConjugator):
    REMOVE = 'oir'
    FUTURE_RADICAL = 'oir' # Go home, French. You're drunk.

@conjugates([u'.*pourvoir'])
class PourvoirConjugator(PrevoirConjugator):
    REMOVE = 'oir'
    SIMPLE_PAST_RADICAL = 'u' # Now we're just getting silly.

@conjugates([u'.*cevoir'])
class CevoirConjugator(IrConjugator):
    REMOVE = 'cevoir'
    PAST_PARTICIPLE = u'çu'
    SINGULAR_RADICAL = u'çoi'
    ATONIC_RADICAL = 'cev'
    TONIC_RADICAL = u'çoiv'
    FUTURE_RADICAL = 'cevr'
    SIMPLE_PAST_RADICAL = u'çu'

# Wow, this verb is a mess.
@conjugates([u'.*asseoir'])
class AsseoirConjugator(IrConjugator):
    REMOVE = 'eoir'
    PAST_PARTICIPLE = 'is'
    SINGULAR_RADICAL = 'ied|oi'
    ATONIC_RADICAL = 'ey|oy'
    TONIC_RADICAL = 'ey|oi'
    FUTURE_RADICAL = u'iér|oir'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*venir', u'circonvenir|contrevenir|prévenir|subvenir|.*tenir', u'convenir'])
class EnirConjugator(IrConjugator):
    REMOVE = 'enir'
    PAST_PARTICIPLE = 'enu'
    SINGULAR_RADICAL = 'ien'
    ATONIC_RADICAL = 'en'
    TONIC_RADICAL = 'ienn'
    FUTURE_RADICAL = 'iendr'
    SIMPLE_PAST_RADICAL = 'i'

    # There's an extra 'n' here, but it comes after any circumflex.  We
    # choose to customize the suffixes instead of the merging rule.
    SIMPLE_PAST_SUFFIXES = \
      ['ns', 'ns', 'nt', u'\u0302nmes', u'\u0302ntes', 'nrent']
    SUBJUNCTIVE_IMPERFECT_SUFFIXES = \
      ['nsse', 'nsses', u'\u0302nt', 'nssions', 'nssiez', 'nssent']

@conjugates([u'.*fuir'])
class FuirConjugator(IrConjugator):
    REMOVE = 'ir'
    SINGULAR_RADICAL = 'i'
    ATONIC_RADICAL = 'y'
    TONIC_RADICAL = 'i'

@conjugates([u'.*ouvrir|.*frir'])
class RirConjugator(IrConjugator):
    REMOVE = 'rir'
    PAST_PARTICIPLE = 'ert'
    SINGULAR_RADICAL = 're'
    ATONIC_RADICAL = 'r'
    TONIC_RADICAL = 'r'

    # This works like a regular -er verb.
    PRESENT_SUFFIXES = ['', 's', '', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['', 'ons', 'ez']

@conjugates([u'.*courir'])
class CourirConjugator(IrConjugator):
    REMOVE = 'ir'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = ''
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'mourir'])
class MourirConjugator(IrConjugator):
    REMOVE = 'ourir'
    PAST_PARTICIPLE = 'ort'
    SINGULAR_RADICAL = 'eur'
    TONIC_RADICAL = 'eur'
    FUTURE_RADICAL = 'ourr'
    SIMPLE_PAST_RADICAL = 'ouru'

@conjugates([u'.*quérir'])
class QuerirConjugator(IrConjugator):
    REMOVE = u'érir'
    PAST_PARTICIPLE = 'is'
    SINGULAR_RADICAL = 'ier'
    TONIC_RADICAL = u'ièr'
    FUTURE_RADICAL = 'err'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*cueillir'])
class CueillirConjugator(IrConjugator):
    REMOVE = 'ir'
    SINGULAR_RADICAL = 'e'
    FUTURE_RADICAL = 'er'

    # This works like a regular -er verb.
    PRESENT_SUFFIXES = ['', 's', '', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['', 'ons', 'ez']
