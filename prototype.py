# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET

# A verb prototype.  Loaded from XML.
class Prototype:
    def __init__(self, element):
        regex = element.get('REGEX')
        self.label = regex.replace("(?'c'", "(")
        new_regex = "(?:%s)$" % regex.replace("(?'c'", "(?P<c>")
        self.regex = re.compile(new_regex)
        self.infinitive = element.get('INFINITIVE')
        self.notes = element.get('NOTES')
        self.radical = element.get('RADICAL')
        self.ending = element.get('ENDING')
        self.aux = element.get('AUX')
        self.ppresent = element.get('PPRESENT')
        self.ppasse = element.get(u'PPASSÉ')
        self.present = element.get(u'PRÉSENT')
        self.imparfait = element.get('IMPARFAIT')
        self.passe = element.get(u'PASSÉ')
        self.futur = element.get('FUTUR')
        self.spresent = element.get(u'SPRÉSENT')
        self.simparfait = element.get('SIMPARFAIT')
        self.imperatif = element.get(u'IMPÉRATIF')
        self.condition = element.get('CONDITION')
        self.example = None # May be filled in by our users.

    def matches(self, infinitive):
        return self.regex.match(infinitive)

    def generate_forms(self, attr):
        forms = []
        for form in getattr(self, attr).split(','):
            alternatives = form.split('|')
            forms.append([self.radical + a for a in alternatives])
        return forms

    def example_past_participles(self):
        return self.generate_forms('ppasse')[0]

    def example_present_particples(self):
        return self.generate_forms('ppresent')[0]

    def example_present(self):
        return self.generate_forms('present')

    def example_imperative(self):
        forms = self.generate_forms('imperatif')
        return [forms[i] for i in [1, 3, 4]]

    def example_imperfect(self):
        return self.generate_forms('imparfait')

    def example_subjunctive(self):
        return self.generate_forms('spresent')

    def example_future(self):
        return self.generate_forms('futur')

    def example_conditional(self):
        return self.generate_forms('condition')

    def example_simple_past(self):
        return self.generate_forms('passe')

    def example_subjunctive_imperfect(self):
        return self.generate_forms('simparfait')
    
# Load our verb prototypes from XML.
_conjugator = ET.parse('verbs-0-2-0.xml').getroot()
PROTOTYPES = [Prototype(p) for p in _conjugator.findall('Prototype')]

# Allow looking up prototypes by label.
BY_LABEL = {}
for p in PROTOTYPES:
    BY_LABEL[p.label] = p
