# -*- coding: utf-8 -*-

from conjugator import *

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

