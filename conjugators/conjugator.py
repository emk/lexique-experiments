# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import defaultdict
from unicodedata import normalize
import re

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

    # Record the label under which we were registered.
    def __init__(self, label=None):
        self.label = label

    # Return a reasonable name for this conjugator.
    def name(self):
        name = self.__class__.__name__.replace('Conjugator', '').lower()
        return name or None

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
        self._assert_matches(prototype, 'present')
        self._assert_matches(prototype, 'present_particples')
        self._assert_matches(prototype, 'imperative')
        self._assert_matches(prototype, 'imperfect')
        self._assert_matches(prototype, 'subjunctive')
        self._assert_matches(prototype, 'future')
        self._assert_matches(prototype, 'conditional')
        self._assert_matches(prototype, 'simple_past')
        self._assert_matches(prototype, 'subjunctive_imperfect')

# Used by default for verb forms we don't handle yet.
class UnimplementedConjugator(Conjugator):
    def name(self):
        return None

    def assert_matches_prototype(self, prototype):
        print("Unimplemented: %s (%s)" % (prototype.example, prototype.label))
        sys.exit(1)

# Look up conjugators by verb label.
BY_LABEL = defaultdict(UnimplementedConjugator)

# A decorator for subclasses of Conjugator, to help register them.
def conjugates(labels):
    def wrap(conjugator_class):
        for label in labels:
            BY_LABEL[label] = conjugator_class(label)
        return conjugator_class
    return wrap
