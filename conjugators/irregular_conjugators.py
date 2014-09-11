# -*- coding: utf-8 -*-

from conjugator import *

# This class doesn't actually conjugate anything.  It just says it does.
# We use this for verbs which are truly irregular.
class IrregularConjugator(Conjugator):
    def summarize(self):
        return "(irregular)"

    def assert_matches_prototype(self, prototype):
        pass

@conjugates([u'être'])
class EtreConjugator(IrregularConjugator):
    pass

@conjugates([u'avoir'])
class AvoirConjugator(IrregularConjugator):
    pass

@conjugates([u'aller'])
class AllerConjugator(IrregularConjugator):
    pass

@conjugates([u'.*faire'])
class FaireConjugator(IrregularConjugator):
    pass

@conjugates([u'pouvoir'])
class PouvoirConjugator(IrregularConjugator):
    pass

@conjugates([u'.*vouloir'])
class VouloirConjugator(IrregularConjugator):
    pass

@conjugates([u'.*savoir'])
class SavoirConjugator(IrregularConjugator):
    pass

@conjugates([u'.*devoir'])
class DevoirConjugator(IrregularConjugator):
    pass

@conjugates([u'falloir'])
class FalloirConjugator(IrregularConjugator):
    pass

@conjugates([u'.*valoir'])
class ValoirConjugator(IrregularConjugator):
    pass

@conjugates(['faillir'])
class FaillirConjugator(IrregularConjugator):
    pass

# TODO: Defective verbs to handle later.
@conjugates([u'.*pleuvoir', u'parfaire', u'.*raire', u'adirer|douer'])
class DefectiveConjugator(IrregularConjugator):
    def summarize(self):
        return "(defective)"

@conjugates(u'.*pleuvoir')
class PleuvoirConjugator(DefectiveConjugator):
    pass

@conjugates(u'parfaire')
class ParfaireConjugator(DefectiveConjugator):
    pass

@conjugates(u'.*raire')
class RaireConjugator(DefectiveConjugator):
    pass

@conjugates(u'adirer|douer')
class DouerConjugator(DefectiveConjugator):
    pass
