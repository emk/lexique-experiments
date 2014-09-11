# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import defaultdict
from unicodedata import normalize
import re

# A decorator which allows only one instance of each subclass to be
# created.  We do things like this because we're deliberately confusing
# classes and intances, which allows us to store quite a few variables like
# PAST_PARTICIPLE on the class, but still easy override methods and update
# variables like example_verb at runtime.
#
# This is a bit of a weird design, but it just fell out.  And hey, I need
# to find out how metaprogramming works in Python, anyway.
def per_subclass_singleton(klass):
    def new(subclass):
        if not '_instance' in subclass.__dict__:
            subclass._instance = object.__new__(subclass)
        return subclass._instance
    def instance(subclass):
        if '_instance' in subclass.__dict__:
            return subclass._instance
        return None
    klass.__new__ = staticmethod(new)
    klass.instance = classmethod(instance)
    return klass

# Conjugate a group of verbs.
@per_subclass_singleton
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

    # Initialize this conjugator.
    def __init__(self):
        self.example_verb = None

    # Find the conjugator we're based off of.
    def parent_conjugator(self):
        assert(self.__class__ != Conjugator)
        return self.__class__.__base__.instance()

    # Let the conjugator know about a verb.
    def register_verb(self, infinitive):
        if self.example_verb is None:
            self.example_verb = infinitive

    # Return a reasonable name for this conjugator.
    def name(self):
        return self.example_verb

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

    # Attach a subject pronoun to a verb form.
    def _prepend_pronoun(self, pronoun, form):
        nf = normalize('NFD', form)
        if pronoun == 'je':
            # TODO: Handle 'h meut'.
            if re.match('^[aeiouh]', nf):
                return "j'" + form
        return pronoun + " " + form

    # Attach a list of pronouns to a list of verb forms.
    def _zip_pronouns(self, pronouns, forms):
        result = []
        for p, vs in zip(pronouns, forms):
            variants = []
            for v in vs:
                variants.append(self._prepend_pronoun(p, v))
            result.append('/'.join(variants))
        return result

    # Generate a list of interesting forms, based on what's actually
    # overriden in this class.  This assumes that the reader knows the
    # basics of French verbs.
    def summarize_forms(self):
        infinitive = self.example_verb

        # Accumulate forms here.
        interesting = []
        def add(pronouns, forms):
            zipped = self._zip_pronouns(pronouns, forms)
            interesting.extend(zipped)

        # Our default pronouns.  We use the masculine forms because they're
        # shorter, and we want to show these summaries in confined spaces.
        pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']

        # Determine which fields have been customized.
        d = self.__class__.__dict__
        def customizes(key):
            return key in d

        # Don't try to figure out the auxiliary verb for the past participle.
        if customizes('PAST_PARTICIPLE'):
            interesting.append('(p.p.) ' +
                               '/'.join(self.past_participles(infinitive)))

        # Show only as many present-tense forms as we need.
        present = self.present(infinitive)
        if customizes('PRESENT_SUFFIXES'):
            add(pronouns, present)
        else:
            if customizes('SINGULAR_RADICAL'):
                add(pronouns[1:2], present[1:2])
            if customizes('ATONIC_RADICAL'):
                add(pronouns[3:4], present[3:4])
            if customizes('TONIC_RADICAL'):
                add(pronouns[5:6], present[5:6])

        # We can infer all future tense forms from one example.
        if 'FUTURE_RADICAL' in d:
            add(pronouns[2:3], self.future(infinitive)[2:3])

        # Show a few simple past forms to give the idea.  The rest can
        # be looked up on the rare chance they're needed.
        if customizes('SIMPLE_PAST_SUFFIXES'):
            add(['(p.s.) il'], self.simple_past(infinitive)[2:3])
            add(pronouns[5:6], self.simple_past(infinitive)[5:6])
        elif customizes('SIMPLE_PAST_RADICAL'):
            add(['(p.s.) il'], self.simple_past(infinitive)[2:3])

        # Return our interesting forms.
        return ', '.join(interesting)

    # Summarize everything interesting we know about this class.
    def summarize(self):
        forms = self.summarize_forms()
        parent = self.parent_conjugator()
        if parent:
            like = parent.example_verb
            if like:
                return u"Like %s, except: %s" % (like, forms)
        return forms

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

# Used by default for verb forms we don't handle yet.  Because of the
# per_subclass_singleton code, there's only one instance of this class
# shared between all unknown verbs.
class UnimplementedConjugator(Conjugator):
    def register_verb(self, infinitive):
        None

    def assert_matches_prototype(self, prototype):
        print("Unimplemented: %s (%s)" % (self.name(), prototype.label))
        sys.exit(1)

# A list of all known conjugators.
ALL = []

# Look up conjugators by verb label.
BY_LABEL = defaultdict(UnimplementedConjugator)

# A decorator for subclasses of Conjugator, to help register them.  If you
# pass in 'independent_conjugators=True', it will create seperate instances
# for each prototype label.
def conjugates(labels):
    def wrap(conjugator_class):
        conjugator = conjugator_class()
        ALL.append(conjugator)
        for label in labels:
            BY_LABEL[label] = conjugator
        return conjugator_class
    return wrap
