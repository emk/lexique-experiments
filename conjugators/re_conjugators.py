# -*- coding: utf-8 -*-

# See http://french.about.com/od/grammar/a/irregular-re-verbs.htm

import re
from conjugator import *

@conjugates([u'.*andre|.*endre|.*ondre|.*erdre|.*ordre|.*eurdre', u'.*ompre'])
class ReConjugator(Conjugator):
    NAME = '-re'

    REMOVE = 're'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*prendre'])
class PrendreConjugator(ReConjugator):
    REMOVE = 'endre'
    PAST_PARTICIPLE = 'is'
    ATONIC_RADICAL = 'en'
    TONIC_RADICAL = 'enn'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*iendre|.*eindre', u'.*aindre', u'.*oindre'])
class NdreConjugator(ReConjugator):
    REMOVE = 'ndre'
    PAST_PARTICIPLE = 'nt'
    SINGULAR_RADICAL = 'n'
    ATONIC_RADICAL = 'gn'
    TONIC_RADICAL = 'gn'
    SIMPLE_PAST_RADICAL = 'gni'

@conjugates([u'résoudre'])
class ResoudreConjugator(ReConjugator):
    REMOVE = 'udre'
    PAST_PARTICIPLE = 'lu'
    SINGULAR_RADICAL = 'u'
    ATONIC_RADICAL = 'lv'
    TONIC_RADICAL = 'lv'
    SIMPLE_PAST_RADICAL = 'lu'

# Verbs like dire, but without the irregular second-person plural.
@conjugates([u'.*dire'])
class IreConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = 't'
    ATONIC_RADICAL = 's'
    TONIC_RADICAL = 's'
    SIMPLE_PAST_RADICAL = ''

@conjugates([u'dire|redire'])
class DireConjugator(IreConjugator):
    # Present 2PL is 'dites'.
    def present(self, infinitive):
        inherited = super(DireConjugator, self).present(infinitive)
        inherited[4] = ['dites']
        return inherited

    # Pick up our change to 'dites'.
    def imperative(self, infinitive):
        present = self.present(infinitive)
        return [present[i] for i in [1,3,4]]

    # Provide a custom summary.
    def summarize_forms(self):
        return 'vous dites'

@conjugates([u'.*lire'])
class LireConjugator(IreConjugator):
    REMOVE = 'ire'
    PAST_PARTICIPLE = 'u'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'.*uire'])
class UireConjugator(IreConjugator):
    REMOVE = 're'
    SIMPLE_PAST_RADICAL = 'si'

@conjugates([u'suffire'])
class SuffireConjugator(IreConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = ''

# Not enough in common with other -ire verbs to lump.
@conjugates([u'.*crire'])
class CrireConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = 't'
    ATONIC_RADICAL = 'v'
    TONIC_RADICAL = 'v'
    SIMPLE_PAST_RADICAL = 'vi'

# Not enough in common with other -ire verbs to lump.
@conjugates([u'.*rire'])
class RireConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = ''
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''
    SIMPLE_PAST_RADICAL = ''

@conjugates([u'.*suivre'])
class SuivreConjugator(ReConjugator):
    REMOVE = 'vre'
    PAST_PARTICIPLE = 'vi'
    SINGULAR_RADICAL = ''

@conjugates([u'.*vivre'])
class VivreConjugator(SuivreConjugator):
    REMOVE = 'ivre'
    PAST_PARTICIPLE = u'écu'
    SIMPLE_PAST_RADICAL = u'écu'

@conjugates([u'.*croire'])
class CroireConjugator(ReConjugator):
    REMOVE = 'oire'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = 'oy'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'.*boire'])
class BoireConjugator(ReConjugator):
    REMOVE = 'oire'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = 'uv'
    TONIC_RADICAL = 'oiv'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates(['.*battre'])
class BattreConjugator(ReConjugator):
    REMOVE = 'tre'
    SINGULAR_RADICAL = ''

@conjugates(['.*mettre'])
class MettreConjugator(BattreConjugator):
    REMOVE = 'ettre'
    PAST_PARTICIPLE = 'is'
    SIMPLE_PAST_RADICAL = 'i'

# TODO: Consider adding a modern 'aitre' version of these infinitives.
@conjugates([u'.*connaître|.*paraître'])
class ConnaitreConjugator(ReConjugator):
    REMOVE = u'aître'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = 'ai'
    ATONIC_RADICAL = 'aiss'
    TONIC_RADICAL = 'aiss'
    SIMPLE_PAST_RADICAL = 'u'

    # The orthographe rectifiée de 1990 drops the cirucmflex from this
    # verb, removing this special case (and also changing the infinitive).
    PRESENT_SUFFIXES = ['s', 's', u'\u0302t', 'ons', 'ez', 'ent']

@conjugates([u'.*naître'])
class NaitreConjugator(ConnaitreConjugator):
    REMOVE = u'aître'
    PAST_PARTICIPLE = u'é'
    SIMPLE_PAST_RADICAL = 'aqui'

@conjugates([u'taire'])
class AireConjugator(ReConjugator):
    REMOVE = u'aire'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = u'ais'
    TONIC_RADICAL = u'ais'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'.*plaire'])
class PlaireConjugator(AireConjugator):
    # Another circumflex adjustment.  If we supported alterantive suffixes,
    # we're just write:
    #     PRESENT_SUFFIXES = ['s', 's', u'\u0302t|t', 'ons', 'ez', 'ent']
    def present(self, infinitive):
        inherited = super(PlaireConjugator, self).present(infinitive)
        inherited[2] = [re.sub('ait$', u'aît', inherited[2][0])] + inherited[2]
        return inherited

    # Provide a custom summary.
    def summarize_forms(self):
        return u'il plaît/il plait'

@conjugates([u'.*vaincre'])
class VaincreConjugator(ReConjugator):
    REMOVE = 'cre'
    SINGULAR_RADICAL = '' # See below.
    ATONIC_RADICAL = 'qu'
    TONIC_RADICAL = 'qu'
    SIMPLE_PAST_RADICAL = 'qui'

    # Handle this here, instead of adding complications to the suffixing
    # algorithm.
    PRESENT_SUFFIXES = ['cs', 'cs', 'c', 'ons', 'ez', 'ent']
    IMPERATIVE_SUFFIXES = ['cs', 'ons', 'ez']

@conjugates([u'.*foutre'])
class FoutreConjugator(ReConjugator):
    # Literary tenses are rare.
    REMOVE = 'tre'
    SINGULAR_RADICAL = ''

@conjugates([u'.*clure'])
class ClureConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = ''
    SIMPLE_PAST_RADICAL = ''
