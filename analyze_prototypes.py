# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import defaultdict
from unicodedata import normalize
import re
import sqlite3
import prototype

# Sources:
#   http://fr.wiktionary.org/wiki/Annexe:Conjugaison_en_fran%C3%A7ais
#   http://www.french-linguistics.co.uk/grammar/irregular_verbs_paradigms.shtml
#   http://french.about.com/od/grammar/a/irregular-re-verbs.htm (and related)

# More big verb families that don't quite follow the rules:
#   dormir: Drop characteristic consonant in present singular.
#   couvrir: Conjugate like -er verbs.
#   prendre: Drops -d- in plural, doubles -n- in third person plural.
#   battre: Drops final -t in singular forms.
#   mettre: Like battre, except past participle and literary tenses.
#   rompre: Like regular -re, except for -t in third person singular.
#   craindre: Drop the -d, change to -gn- in plural.

# Conjugate a group of verbs.
class Conjugator(object):
    REMOVE = None
    PAST_PARTICIPLE = None
    SINGULAR_RADICAL = None
    ATONIC_RADICAL = None
    TONIC_RADICAL = None
    FUTURE_RADICAL = None
    SIMPLE_PAST_RADICAL = None

    # Search up the class hierarchy for the specified key.  If it is found,
    # optionally return a related key from the same level of the class
    # hierarchy.  This is used to search for radicals
    def _find_key(self, key, key2=None):
        klass = self.__class__
        while not key in klass.__dict__ and klass != Conjugator:
            klass = klass.__base__
        if key in klass.__dict__ and getattr(klass, key) is not None:
            if key2 is not None:
                if key2 in klass.__dict__ and getattr(klass, key2) is not None:
                    return (getattr(klass, key), getattr(klass, key2))
                raise KeyError(key2)
            return getattr(klass, key)
        else:
            raise KeyError(key)

    # Construct the specified list of radicals for the given infinitive.
    # Returns a list because of verbs which have alternative versions of
    # certain radicals.
    def _radicals(self, key, infinitive):
        (radicals, remove) = self._find_key(key, 'REMOVE')
        return [re.sub(remove+u'$', r, infinitive) for r in radicals.split('|')]

    def past_participles(self, infinitive):
        return self._radicals('PAST_PARTICIPLE', infinitive)

    def present_particples(self, infinitive):
        atonic_r = self.atonic_radicals(infinitive)
        return self._simple_forms(atonic_r, ['ant'])[0]

    def singular_radicals(self, infinitive):
        return self._radicals('SINGULAR_RADICAL', infinitive)

    def atonic_radicals(self, infinitive):
        return self._radicals('ATONIC_RADICAL', infinitive)

    def tonic_radicals(self, infinitive):
        return self._radicals('TONIC_RADICAL', infinitive)

    def future_radicals(self, infinitive):
        return self._radicals('FUTURE_RADICAL', infinitive)

    def simple_past_radicals(self, infinitive):
        return self._radicals('SIMPLE_PAST_RADICAL', infinitive)

    # General suffix application rules that simplify life elsewhere.
    def _apply_suffix(self, radical, suffix):
        if re.search('g$', radical) and not re.search(u'^[ieéè]', suffix):
            # Preserve 'g' sounds.
            radical = radical + u'e'
        elif re.search('d$', radical) and suffix == u't':
            # Assimilate trailing 't' suffixes.
            suffix = u''
        # Normalize Unicode to support simple_past_radicals which begin
        # with a combining cicumflex.
        return normalize('NFC', unicode(radical+suffix))

    # Given pairs of radical lists and endings, generate all forms.
    def _forms(self, patterns):
        return [[self._apply_suffix(r, s) for r in radicals]
                for (radicals,s) in patterns]

    # Generate a set of forms which all use the same radical.
    def _simple_forms(self, radicals, suffixes):
        return self._forms([(radicals, s) for s in suffixes])

    # Suffixes used by the present tense.
    def present_suffixes(self):
        return ['s', 's', 't', 'ons', 'ez', 'ent']

    # Generate present tense forms.
    def present(self, infinitive):
        sing_r = self.singular_radicals(infinitive)
        atonic_r = self.atonic_radicals(infinitive)
        tonic_r = self.tonic_radicals(infinitive)
        s = self.present_suffixes()
        return self._forms([
            (sing_r, s[0]), (sing_r, s[1]), (sing_r, s[2]),
            (atonic_r, s[3]), (atonic_r, s[4]), (tonic_r, s[5])])

    # Generate imperative forms.
    def imperative(self, infinitive):
        present = self.present(infinitive)
        return [present[1], present[3], present[4]]

    # Generate imperfect forms.
    def imperfect(self, infinitive):
        atonic_r = self.atonic_radicals(infinitive)
        suffixes = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        return self._simple_forms(atonic_r, suffixes)

    # Generate subjunctive forms.
    def subjunctive(self, infinitive):
        tonic_r = self.tonic_radicals(infinitive)
        atonic_r = self.atonic_radicals(infinitive)
        return self._forms([
            (tonic_r, 'e'), (tonic_r, 'es'), (tonic_r, 'e'),
            (atonic_r, 'ions'), (atonic_r, 'iez'), (tonic_r, 'ent')])

    # Generate future forms.
    def future(self, infinitive):
        future_r = self.future_radicals(infinitive)
        suffixes = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
        return self._simple_forms(future_r, suffixes)

    # Generate conditional forms.
    def conditional(self, infinitive):
        future_r = self.future_radicals(infinitive)
        suffixes = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        return self._simple_forms(future_r, suffixes)

    # Suffixes used by the simple past tense.  These may begin with
    # Unicode combining characters.
    def simple_past_suffixes(self):
        return ['s', 's', 't', u'\u0302mes', u'\u0302tes', u'rent']

    # Generate the simple past tense forms.
    def simple_past(self, infinitive):
        past_r = self.simple_past_radicals(infinitive)
        suffixes = self.simple_past_suffixes()
        return self._simple_forms(past_r, suffixes)

    # Suffixes used by the simple past tense.  These may begin with
    # Unicode combining characters.
    def subjunctive_imperfect_suffixes(self):
        return ['sse', 'sses', u'\u0302t', 'ssions', 'ssiez', 'ssent']

    # Generate the subjunctive imperfect forms.
    def subjunctive_imperfect(self, infinitive):
        past_r = self.simple_past_radicals(infinitive)
        suffixes = self.subjunctive_imperfect_suffixes()
        return self._simple_forms(past_r, suffixes)

    # Called internally to compare verb forms with a Prototype object.
    def _assert_matches(self, prototype, method_name):
        expected = getattr(prototype, 'example_' + method_name)()
        got = getattr(self, method_name)(prototype.infinitive)
        if expected != got:
            err = (u"Mismatch for %s of %s (%s)\n  Expected: %s\n  Got: %s" %
                   (method_name, prototype.infinitive, prototype.label,
                    expected, got))
            print(err, file=sys.stderr)
            raise AssertionError()

    # Generate all verb forms and ensure they match those generated by
    # the specified Prototype object.
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

# Used by default for verb forms we don't handle yet.
class UnimplementedConjugator(Conjugator):
    def assert_matches_prototype(self, prototype):
        print("Unimplemented: %s (%s)" % (p.example, p.label))
        sys.exit(1)
        
# Look up conjugators by verb label.
CONJUGATOR_BY_LABEL = defaultdict(UnimplementedConjugator)

# This class doesn't actually conjugate anything.  It just says it does.
# We use this for verbs which are truly irregular.
class IrregularConjugator:
    def assert_matches_prototype(self, prototype):
        pass

CONJUGATOR_BY_LABEL[u'être'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'avoir'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'aller'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'.*faire'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'pouvoir'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'.*vouloir'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'.*savoir'] = IrregularConjugator()
CONJUGATOR_BY_LABEL[u'.*voir|.*oir'] = IrregularConjugator() # TODO: Replace.
CONJUGATOR_BY_LABEL[u'.*venir'] = IrregularConjugator() # TODO: Replace.
CONJUGATOR_BY_LABEL[u'.*devoir'] = IrregularConjugator()

class ErConjugator(Conjugator):
    REMOVE = 'er'
    PAST_PARTICIPLE = u'é'
    SINGULAR_RADICAL = 'e'
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''
    FUTURE_RADICAL = 'er'
    # We put the 'a' into our endings, because of 'èrent'.
    SIMPLE_PAST_RADICAL = ''

    def present_suffixes(self):
        return ['', 's', '', 'ons', 'ez', 'ent']

    def imperative(self, infinitive):
        inherited = super(ErConjugator, self).imperative(infinitive)
        sing_r = self.singular_radicals(infinitive)
        return [sing_r] + inherited[1:]

    def simple_past_suffixes(self):
        return ['ai', 'as', 'a', u'âmes', u'âtes', u'èrent']

    def subjunctive_imperfect_suffixes(self):
        return ['asse', 'asses', u'ât', 'assions', 'assiez', 'assent']

CONJUGATOR_BY_LABEL[u'.*er'] = ErConjugator()
CONJUGATOR_BY_LABEL[u'arriver|entrer|rentrer|rester|retomber|tomber'] = \
  ErConjugator() # être verbs.
CONJUGATOR_BY_LABEL[u'.*ger'] = ErConjugator()

class IrConjugator(Conjugator):
    REMOVE = 'r'
    PAST_PARTICIPLE = ''
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = 'ss'
    TONIC_RADICAL = 'ss'
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = ''
    
CONJUGATOR_BY_LABEL[u'.*ir'] = IrConjugator()

class ReConjugator(Conjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = 'i'

CONJUGATOR_BY_LABEL[u'.*andre|.*endre|.*ondre|.*erdre|.*ordre|.*eurdre'] = \
  ReConjugator()

class PrendreConjugator(ReConjugator):
    REMOVE = 'endre'
    PAST_PARTICIPLE = 'is'
    ATONIC_RADICAL = 'en'
    TONIC_RADICAL = 'enn'
    SIMPLE_PAST_RADICAL = 'i'

CONJUGATOR_BY_LABEL[u'.*prendre'] = PrendreConjugator() # TODO: Replace.

class DireConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = 't'
    ATONIC_RADICAL = 's'
    TONIC_RADICAL = 's'
    SIMPLE_PAST_RADICAL = ''

    def present(self, infinitive):
        inherited = super(DireConjugator, self).present(infinitive)
        inherited[4] = ['dites']
        return inherited

CONJUGATOR_BY_LABEL[u'.*dire'] = DireConjugator()

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
    conj.assert_matches_prototype(p)
