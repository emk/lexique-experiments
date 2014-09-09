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

    # Suffixes used by the present tense.
    PRESENT_SUFFIXES = ['s', 's', 't', 'ons', 'ez', 'ent']

    # Suffixes used by the imperative.
    IMPERATIVE_SUFFIXES = ['s', 'ons', 'ez']

    # Suffixes used by the simple past tense.  These may begin with
    # Unicode combining characters.
    SIMPLE_PAST_SUFFIXES = ['s', 's', 't', u'\u0302mes', u'\u0302tes', u'rent']

    # Suffixes used by the subjunctive imperfect tense.  These may begin
    # with Unicode combining characters.
    SUBJUNCTIVE_IMPERFECT_SUFFIXES = \
      ['sse', 'sses', u'\u0302t', 'ssions', 'ssiez', 'ssent']

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

    def present_suffixes(self):
        return self._find_key('PRESENT_SUFFIXES')

    def imperative_suffixes(self):
        return self._find_key('IMPERATIVE_SUFFIXES')

    def simple_past_suffixes(self):
        return self._find_key('SIMPLE_PAST_SUFFIXES')

    def subjunctive_imperfect_suffixes(self):
        return self._find_key('SUBJUNCTIVE_IMPERFECT_SUFFIXES')

    # General suffix application rules that simplify life elsewhere.
    def _apply_suffix(self, radical, suffix):
        soft_vowels = u'^[ieéè]'
        if re.search('g$', radical) and not re.search(soft_vowels, suffix):
            # Preserve soft 'g' sounds.
            radical = radical + u'e'
        elif re.search('c$', radical) and not re.search(soft_vowels, suffix):
            # Preserve soft 'c' sounds.
            radical = re.sub('c$', u'ç', radical)
        elif re.search('[dt]$', radical) and suffix == u't':
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
        sing_r = self.singular_radicals(infinitive)
        atonic_r = self.atonic_radicals(infinitive)
        s = self.imperative_suffixes()
        return self._forms([
            (sing_r, s[0]), (atonic_r, s[1]), (atonic_r, s[2])])

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

    # Generate the simple past tense forms.
    def simple_past(self, infinitive):
        past_r = self.simple_past_radicals(infinitive)
        suffixes = self.simple_past_suffixes()
        return self._simple_forms(past_r, suffixes)

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

# A decorator for subclasses of Conjugator, to help register them.
def conjugates(labels):
    def wrap(conjugator_class):
        for label in labels:
            CONJUGATOR_BY_LABEL[label] = conjugator_class()
        return conjugator_class
    return wrap

# This class doesn't actually conjugate anything.  It just says it does.
# We use this for verbs which are truly irregular.
@conjugates([u'être', u'avoir', u'aller', u'.*faire', u'pouvoir', u'.*vouloir',
             u'.*savoir', u'.*devoir'])
@conjugates([u'falloir']) # TODO: Defective verbs to handle later.
class IrregularConjugator:
    def assert_matches_prototype(self, prototype):
        pass

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

@conjugates([u'.*é([djlmnprsty])er'])
class ErerConjugator(ErConjugator):
    REMOVE = u'é([djlmnprsty])er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'

@conjugates([u'.*e([mnprsv])er'])
class EmerConjugator(ErConjugator):
    REMOVE = 'e([mnprsv])er'
    SINGULAR_RADICAL = u'è\\1e'
    TONIC_RADICAL = u'è\\1'
    FUTURE_RADICAL = u'è\\1er'

@conjugates([u'.*ayer'])
class AyerConjugator(ErConjugator):
    REMOVE = 'yer'
    SINGULAR_RADICAL = 'ie|ye'
    TONIC_RADICAL = 'i|y'
    FUTURE_RADICAL = 'ier|yer'

@conjugates([u'.*ir'])
class IrConjugator(Conjugator):
    REMOVE = 'r'
    PAST_PARTICIPLE = ''
    SINGULAR_RADICAL = ''
    ATONIC_RADICAL = 'ss'
    TONIC_RADICAL = 'ss'
    FUTURE_RADICAL = 'r'
    SIMPLE_PAST_RADICAL = ''

class IrWithoutIssConjugator(IrConjugator):
    REMOVE = 'ir'
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''

@conjugates([u'.*voir|.*oir'])
class VoirConjugator(IrWithoutIssConjugator):
    REMOVE = 'oir'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = 'oy'
    TONIC_RADICAL = 'oi'
    FUTURE_RADICAL = 'err'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*venir', u'circonvenir|contrevenir|prévenir|subvenir|.*tenir'])
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

@conjugates([u'partir'])
class PatrirConjugator(IrWithoutIssConjugator):
    REMOVE = 'tir'
    SINGULAR_RADICAL = ''

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

@conjugates([u'.*andre|.*endre|.*ondre|.*erdre|.*ordre|.*eurdre'])
class ReConjugator(Conjugator):
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

@conjugates([u'.*dire'])
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

    # Pick up our change to 'dites'.
    def imperative(self, infinitive):
        present = self.present(infinitive)
        return [present[i] for i in [1,3,4]]

@conjugates([u'.*suivre'])
class SuivreConjugator(ReConjugator):
    REMOVE = 'vre'
    PAST_PARTICIPLE = 'vi'
    SINGULAR_RADICAL = ''

@conjugates([u'.*croire'])
class CroireConjugator(ReConjugator):
    REMOVE = 'oire'
    PAST_PARTICIPLE = 'u'
    ATONIC_RADICAL = 'oy'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates(['.*mettre'])
class MettreConjugator(ReConjugator):
    REMOVE = 'ettre'
    PAST_PARTICIPLE = 'is'
    SINGULAR_RADICAL = 'et'
    SIMPLE_PAST_RADICAL = 'i'

@conjugates([u'.*connaître|.*paraître'])
class ConnaitreConjugator(ReConjugator):
    REMOVE = u'aître'
    PAST_PARTICIPLE = 'u'
    SINGULAR_RADICAL = 'ai'
    ATONIC_RADICAL = 'aiss'
    TONIC_RADICAL = 'aiss'
    SIMPLE_PAST_RADICAL = 'u'

    # The orthographe rectifiée de 1990 drops the cirucmflex from this
    # verb, removing this special case.
    def present(self, infinitive):
        inherited = super(ConnaitreConjugator, self).present(infinitive)
        inherited[2][0] = re.sub('ait$', u'aît', inherited[2][0])
        return inherited

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