# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import defaultdict
from unicodedata import normalize
import re

# Sources:
#   http://fr.wiktionary.org/wiki/Annexe:Conjugaison_en_fran%C3%A7ais
#   http://www.french-linguistics.co.uk/grammar/irregular_verbs_paradigms.shtml
#   http://french.about.com/od/grammar/a/irregular-re-verbs.htm (and related)

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
    def assert_matches_prototype(self, prototype):
        print("Unimplemented: %s (%s)" % (prototype.example, prototype.label))
        sys.exit(1)

# Look up conjugators by verb label.
BY_LABEL = defaultdict(UnimplementedConjugator)

# A decorator for subclasses of Conjugator, to help register them.
def conjugates(labels):
    def wrap(conjugator_class):
        for label in labels:
            BY_LABEL[label] = conjugator_class()
        return conjugator_class
    return wrap

# This class doesn't actually conjugate anything.  It just says it does.
# We use this for verbs which are truly irregular.
@conjugates([u'être', u'avoir', u'aller', u'.*faire', u'pouvoir', u'.*vouloir',
             u'.*savoir', u'.*devoir', u'falloir', u'.*valoir', 'faillir'])
class IrregularConjugator(Conjugator):
    def assert_matches_prototype(self, prototype):
        pass

# TODO: Defective verbs to handle later.
@conjugates([u'.*pleuvoir', u'parfaire', u'.*raire', u'adirer|douer'])
class DefectiveConjugator(IrregularConjugator):
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
    
@conjugates([])
class PleuvoirConjugator(IrregularConjugator):
    # Defective verb.
    pass
#class PleuvoirConjugator(IrWithoutIssConjugator):
#    REMOVE = 'euvoir'
#    PAST_PARTICIPLE = 'u'
#    SINGULAR_RADICAL = 'eu'

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


@conjugates([u'.*andre|.*endre|.*ondre|.*erdre|.*ordre|.*eurdre', u'.*ompre'])
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
class IreConjugator(ReConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = 't'
    ATONIC_RADICAL = 's'
    TONIC_RADICAL = 's'
    SIMPLE_PAST_RADICAL = ''

@conjugates([u'.*dire'])
class DireConjugator(IreConjugator):
    def present(self, infinitive):
        inherited = super(DireConjugator, self).present(infinitive)
        inherited[4] = ['dites']
        return inherited

    # Pick up our change to 'dites'.
    def imperative(self, infinitive):
        present = self.present(infinitive)
        return [present[i] for i in [1,3,4]]

@conjugates([u'.*lire'])
class LireConjugator(IreConjugator):
    REMOVE = 'ire'
    PAST_PARTICIPLE = 'u'
    SIMPLE_PAST_RADICAL = 'u'

@conjugates([u'.*uire'])
class UireConjugator(IreConjugator):
    REMOVE = 're'
    SIMPLE_PAST_RADICAL = 'si'

@conjugates([u'.*crire'])
class CrireConjugator(IreConjugator):
    REMOVE = 're'
    ATONIC_RADICAL = 'v'
    TONIC_RADICAL = 'v'
    SIMPLE_PAST_RADICAL = 'vi'

@conjugates([u'suffire'])
class SuffireConjugator(IreConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = ''

@conjugates([u'.*rire'])
class RireConjugator(IreConjugator):
    REMOVE = 're'
    PAST_PARTICIPLE = ''
    ATONIC_RADICAL = ''
    TONIC_RADICAL = ''

# Neil Coffey says this is similar to the dormir pattern.
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

@conjugates([u'.*vivre'])
class VivreConjugator(SuivreConjugator):
    REMOVE = 'ivre'
    PAST_PARTICIPLE = u'écu'
    SIMPLE_PAST_RADICAL = u'écu'

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
