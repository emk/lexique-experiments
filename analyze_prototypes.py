# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import defaultdict
from unicodedata import normalize
import re
import sqlite3
import prototype

# Sources:
#   http://www.french-linguistics.co.uk/grammar/irregular_verbs_paradigms.shtml
#   http://french.about.com/od/grammar/a/irregular-re-verbs.htm (and related)

# Don't even try to find patterns here. The first four are entirely
# irregular, the latter three we might be able to something with at some
# point.
HIGHLY_IRREGULAR = ['être', 'avoir', 'aller', 'faire', 'pouvoir', 'vouloir',
                    'savoir']

# The "official" regular endings.
GROUP_ER_PRESENT_ENDINGS = ['e', 'es', 'e', 'ons', 'ez', 'ent']
GROUP_IR_PRESENT_ENDINGS = ['is', 'is', 'it', 'ions', 'issez', 'issent']
GROUP_RE_PRESENT_ENDINGS = ['s', 's', '', 'ons', 'ez', 'ent']

# More big verb groups:
#   dormir: Drop characteristic consonant in present singular.
#   couvrir: Conjugate like -er verbs.
#   prendre: Drops -d- in plural, doubles -n- in third person plural.
#   battre: Drops final -t in singular forms.
#   mettre: Like battre, except past participle and literary tenses.
#   rompre: Like regular -re, except for -t in third person singular.
#   craindre: Drop the -d, change to -gn- in plural.

# Conjugate a group of verbs.
class Conjugator:
    def is_implemented(self):
        return False

    def past_participles(self, infinitive):
        raise NotImplementedError()

    def present_particples(self, infinitive):
        return [r + "ant" for r in self.atonic_radicals(infinitive)]

    def singular_radicals(self, infinitive):
        raise NotImplementedError()

    def atonic_radicals(self, infinitive):
        raise NotImplementedError()

    def tonic_radicals(self, infinitive):
        raise NotImplementedError()

    def future_radicals(self, infinitive):
        raise NotImplementedError()

    def simple_past_radicals(self, infinitive):
        raise NotImplementedError()

    # Like simple_past_radicals, but add a cicumflex to the stem.
    #def simple_past_circumflex_radicals(self, infinitive):
    #    past_r = self.simple_past_radicals(infinitive)
    #    # Add a combining circumflex, then normalize to get a regular
    #    # composed character.
    #    return [normalize('NFC', r + u'\u0302') for r in past_r]

    def present(self, infinitive):
        raise NotImplementedError()

    def imperative(self, infinitive):
        raise NotImplementedError()

    def imperfect(self, infinitive):
        raise NotImplementedError()

    def subjunctive(self, infinitive):
        raise NotImplementedError()

    def future(self, infinitive):
        raise NotImplementedError()

    def conditional(self, infinitive):
        raise NotImplementedError()

    def simple_past(self, infinitive):
        raise NotImplementedError()

    def subjunctive_imperfect(self, infinitive):
        raise NotImplementedError()

    def _assert_matches(self, prototype, method_name):
        expected = getattr(prototype, 'example_' + method_name)()
        got = getattr(self, method_name)(prototype.infinitive)
        if expected != got:
            err = (u"Mismatch for %s of %s (%s)\n  Expected: %s\n  Got: %s" %
                   (method_name, prototype.infinitive, prototype.label,
                    expected, got))
            raise AssertionError(err)

    def assert_matches_prototype(self, prototype):
        self._assert_matches(prototype, 'past_participles')
        self._assert_matches(prototype, 'present_particples')
        self._assert_matches(prototype, 'present')
        self._assert_matches(prototype, 'imperative')
        self._assert_matches(prototype, 'imperfect')
        self._assert_matches(prototype, 'subjunctive')
        self._assert_matches(prototype, 'future')
        self._assert_matches(prototype, 'conditional')
        self._assert_matches(prototype, 'simple_past')
        self._assert_matches(prototype, 'subjunctive_imperfect')

# Look up conjugators by verb label.
CONJUGATOR_BY_LABEL = defaultdict(Conjugator)

# This class doesn't actually conjugate anything.  It just says it does.
# We use this for verbs which are truly irregular.
class IrregularConjugator:
    def is_implemented(self):
        return True

    def assert_matches_prototype(self, prototype):
        pass

CONJUGATOR_BY_LABEL[u'être'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'avoir'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'aller'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'.*faire'] = IrregularConjugator()

class ErConjugator(Conjugator):
    def is_implemented(self):
        return True

    def past_participles(self, infinitive):
        return [re.sub(u'er$', u'é', infinitive)]

    def singular_radicals(self, infinitive):
        return [re.sub(u'er$', u'e', infinitive)]

    def atonic_radicals(self, infinitive):
        return [re.sub(u'er$', u'', infinitive)]

    def tonic_radicals(self, infinitive):
        return [re.sub(u'er$', u'', infinitive)]

    def future_radicals(self, infinitive):
        return [infinitive]

    # TODO: We should consider including the 'a'.
    def simple_past_radicals(self, infinitive):
        return [re.sub(u'er$', u'', infinitive)]

    def present(self, infinitive):
        sing_r = self.singular_radicals(infinitive)
        atonic_r = self.atonic_radicals(infinitive)
        tonic_r = self.tonic_radicals(infinitive)
        return [sing_r, [r+'s' for r in sing_r], sing_r,
                [r+'ons' for r in atonic_r],
                [r+'ez' for r in atonic_r],
                [r+'ent' for r in tonic_r]]

    def imperative(self, infinitive):
        sing_r = self.singular_radicals(infinitive)
        present = self.present(infinitive)
        return [sing_r, present[3], present[4]]

    def imperfect(self, infinitive):
        atonic_r = self.atonic_radicals(infinitive)
        suffixes = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        return [[r+s for r in atonic_r] for s in suffixes]

    def subjunctive(self, infinitive):
        tonic_r = self.tonic_radicals(infinitive)
        atonic_r = self.atonic_radicals(infinitive)
        return [[r+'e' for r in tonic_r],
                [r+'es' for r in tonic_r],
                [r+'e' for r in tonic_r],
                [r+'ions' for r in atonic_r],
                [r+'iez' for r in atonic_r],
                [r+'ent' for r in tonic_r]]

    def future(self, infinitive):
        future_r = self.future_radicals(infinitive)
        suffixes = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
        return [[r+s for r in future_r] for s in suffixes]

    def conditional(self, infinitive):
        future_r = self.future_radicals(infinitive)
        suffixes = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        return [[r+s for r in future_r] for s in suffixes]

    def simple_past(self, infinitive):
        past_r = self.simple_past_radicals(infinitive)
        suffixes = ['ai', 'as', 'a', u'âmes', u'âtes', u'èrent']
        return [[r+s for r in past_r] for s in suffixes]

    def subjunctive_imperfect(self, infinitive):
        past_r = self.simple_past_radicals(infinitive)
        suffixes = ['asse', 'asses', u'ât', 'assions', 'assiez', 'assent']
        return [[r+s for r in past_r] for s in suffixes]

CONJUGATOR_BY_LABEL[u'.*er'] = ErConjugator()

# Open our database.
db = sqlite3.connect("lexique.sqlite3")

# Order our prototypes by coverage.
prototypes = []
query = """
SELECT prototype FROM verbe
  WHERE prototype IS NOT NULL
  GROUP BY prototype
  ORDER BY SUM(freqfilms2) DESC"""
for row in db.execute(query):
    prototypes.append(prototype.BY_LABEL[row[0]])

# Load example verbs for our prototypes.
query = """
SELECT prototype, lemme FROM verbe
  WHERE prototype IS NOT NULL
  ORDER BY freqfilms2 DESC"""
for row in db.execute(query):
    label, lemme = row
    p = prototype.BY_LABEL[label]
    if p.example is None:
        p.example = lemme

# Iterate over our prototypes until we hit a mismatch.
for p in prototypes:
    conj = CONJUGATOR_BY_LABEL[p.label]
    if not conj.is_implemented():
        print("Unimplemented: %s (%s)" % (p.example, p.label))
        sys.exit(1)
    conj.assert_matches_prototype(p)
