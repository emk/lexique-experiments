# -*- coding: utf-8 -*-

import re
from conjugator import *

@conjugates([u'.*ir'])
class IrConjugator(Conjugator):
    REMOVE = 'r'
    PAST_PARTICIPLE = ''
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = 'ss'
    TONIC_RADICAL = 'ss'
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = ''

@conjugates([u'bénir'])
class BenirConjugator(IrConjugator):
    REMOVE = 'r'
    PAST_PARTICIPLE = '|t'

class IrWithoutIssConjugator(IrConjugator):
    REMOVE = 'ir'
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''

@conjugates([u'partir', u'sortir', u'ressortir|.*mentir|.*sentir|.*partir',
             u'.*dormir', u'.*servir', 'mentir', '.*endormir|redormir'])
class TirConjugator(IrWithoutIssConjugator):
    REMOVE = '[tmv]ir'
    SINGULAR_RADICAL = ''

@conjugates([u'.*voir|.*oir'])
class VoirConjugator(IrWithoutIssConjugator):
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
class CevoirConjugator(IrWithoutIssConjugator):
    REMOVE = 'cevoir'
    PAST_PARTICIPLE = u'çu'
    SINGULAR_RADICAL = u'çoi'
    ATONIC_RADICAL = 'cev'
    TONIC_RADICAL = u'çoiv'
    FUTURE_RADICAL = 'cevr'
    SIMPLE_PAST_RADICAL = u'çu'

@conjugates([u'.*asseoir'])
class AsseoirConjugator(IrWithoutIssConjugator):
    REMOVE = 'eoir'
    PAST_PARTICIPLE = 'is'
    SINGULAR_RADICAL = 'ied|oi'
    ATONIC_RADICAL = 'ey|oy'
    TONIC_RADICAL = 'ey|oi'
    FUTURE_RADICAL = u'iér|oir'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*venir', u'circonvenir|contrevenir|prévenir|subvenir|.*tenir', u'convenir'])
class EnirConjugator(IrWithoutIssConjugator):
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
class FuirConjugator(IrWithoutIssConjugator):
    REMOVE = 'ir'
    SINGULAR_RADICAL = 'i'
    ATONIC_RADICAL = 'y'
    TONIC_RADICAL = 'i'

@conjugates([u'.*ouvrir|.*frir'])
class RirConjugator(IrWithoutIssConjugator):
    REMOVE = 'rir'
    PAST_PARTICIPLE = 'ert'
    SINGULAR_RADICAL = 're'
    ATONIC_RADICAL = 'r'
    TONIC_RADICAL = 'r'

    # This works like a regular -er verb.
    PRESENT_SUFFIXES = ['', 's', '', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['', 'ons', 'ez']

@conjugates([u'.*courir'])
class CourirConjugator(IrWithoutIssConjugator):
    REMOVE = 'ir'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = ''
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'mourir'])
class MourirConjugator(IrWithoutIssConjugator):
    REMOVE = 'ourir'
    PAST_PARTICIPLE = 'ort'
    SINGULAR_RADICAL = 'eur'
    TONIC_RADICAL = 'eur'
    FUTURE_RADICAL = 'ourr'
    SIMPLE_PAST_RADICAL = 'ouru'

@conjugates([u'.*quérir'])
class QuerirConjugator(IrWithoutIssConjugator):
    REMOVE = u'érir'
    PAST_PARTICIPLE = 'is'
    SINGULAR_RADICAL = 'ier'
    TONIC_RADICAL = u'ièr'
    FUTURE_RADICAL = 'err'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*haïr'])
class HairConjugator(IrConjugator):
    REMOVE = u'ïr'
    SINGULAR_RADICAL = 'i'

    # The usual endings, but without the combining circumflex.
    SIMPLE_PAST_SUFFIXES = ['s', 's', 't', u'mes', u'tes', u'rent']
    SUBJUNCTIVE_IMPERFECT_SUFFIXES = \
      ['sse', 'sses', u't', 'ssions', 'ssiez', 'ssent']

@conjugates([u'.*cueillir'])
class CueillirConjugator(IrWithoutIssConjugator):
    REMOVE = 'ir'
    SINGULAR_RADICAL = 'e'
    FUTURE_RADICAL = 'er'

    # This works like a regular -er verb.
    PRESENT_SUFFIXES = ['', 's', '', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['', 'ons', 'ez']
