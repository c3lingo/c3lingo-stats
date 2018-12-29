#!/usr/bin/env python3

import unittest
from textwrap import dedent
from datetime import timedelta
from parse import parse_block, TranslationShift

class TestTranslationShift(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(TranslationShift('name', 'lang'), TranslationShift('name', 'lang'))
        self.assertNotEqual(TranslationShift('name', 'lang'), TranslationShift('anonther_name', 'lang'))
        self.assertNotEqual(TranslationShift('name', 'lang'), TranslationShift('name', 'anonther_lang'))

class TestParseBlock(unittest.TestCase):

    def test_simple(self):
        result = parse_block(dedent("""
        #1
        [de] 11:00 +00:30, Adams
        Opening Event
        rufus, rixx
        Fahrplan: https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9985.html
        Slides (if available): https://speakers.c3lingo.org/talks/15f4e5c5-40e1-4c73-8da0-4cc2a773ab13/
        → en: waffle, simplysaym, sirenensang
        → fr: informancer, ironic, yann0u
        """))
        self.assertEqual(result.language, 'de')
        self.assertEqual(result.room, 'Adams')
        self.assertEqual(result.duration, timedelta(hours=0, minutes=30))
        self.assertEqual(result.title, 'Opening Event')
        self.assertEqual(result.speakers, ['rufus', 'rixx'])
        self.assertEqual(result.fahrplan, 'https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9985.html')
        self.assertEqual(result.translation_shifts, [
            TranslationShift('waffle', 'en', result),
            TranslationShift('simplysaym', 'en', result),
            TranslationShift('sirenensang', 'en', result),
            TranslationShift('informancer', 'fr', result),
            TranslationShift('ironic', 'fr', result),
            TranslationShift('yann0u', 'fr', result),
        ])

    def test_notes(self):
        """
        Test that notes and parenthetical stuff inside the shift assignments is stripped out
        as much as possible
        """
        result = parse_block(dedent("""
        #31
        [de] 18:50 +01:00, Borg
        "Das ist mir nicht erinnerlich." − Der NSU-Komplex heute
        Caro Keller (NSU-Watch)
        Fahrplan: https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9766.html
        Slides (if available): https://speakers.c3lingo.org/talks/a12d17e9-3758-4fa0-b612-0c6ba22ea773/
        → en: tr1 (note), (foo) tr2
        → fr: tr3 – yay!
        → gsw: (reservation), (another one) , (never mind me)
        """))
        self.assertEqual(result.translation_shifts, [
            TranslationShift('tr1', 'en', result),
            TranslationShift('tr2', 'en', result),
            TranslationShift('tr3', 'fr', result),
        ])

    def test_trailing_comma(self):
        """
        Test that trailing commas don't cause trouble
        """
        result = parse_block(dedent("""
        #31
        [de] 18:50 +01:00, Borg
        "Das ist mir nicht erinnerlich." − Der NSU-Komplex heute
        Caro Keller (NSU-Watch)
        Fahrplan: https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9766.html
        Slides (if available): https://speakers.c3lingo.org/talks/a12d17e9-3758-4fa0-b612-0c6ba22ea773/
        → en: tr1, tr2,
        """))
        self.assertEqual(result.translation_shifts, [
            TranslationShift('tr1', 'en', result),
            TranslationShift('tr2', 'en', result),
        ])



if __name__ == '__main__':
    unittest.main()
