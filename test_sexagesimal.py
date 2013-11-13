from unittest import TestCase
from sexagesimal import Sexagesimal
from flask import Markup

__author__ = 'johnvining'


class TestSexagesimal(TestCase):

    def test_Sexagesimal_init(self):

        test_cases = [
            [Sexagesimal('1'),    Sexagesimal(1), ''],
            [Sexagesimal('1'),    Sexagesimal('1'), ''],
            [Sexagesimal('1'),    Sexagesimal(whole=1, parts=[]), ''],

            [Sexagesimal('1;15'), Sexagesimal('1;15'), ''],
            [Sexagesimal('1;15'), Sexagesimal(1.25), ''],
            [Sexagesimal('1;15'), Sexagesimal('1.25'), ''],
            [Sexagesimal('1;15'), Sexagesimal(whole=1, parts=[15]), ''],

            [Sexagesimal('0;15'), Sexagesimal('0;15'), ''],
            [Sexagesimal('0;15'), Sexagesimal(0.25), ''],
            [Sexagesimal('0;15'), Sexagesimal('0.25'), ''],
            [Sexagesimal('0;15'), Sexagesimal(whole=0, parts=[15]), ''],

            [Sexagesimal('0;15,10,5'), Sexagesimal(whole=0, parts=[15,10,5]),
             'Multiple place __init__ fails.'],

            [Sexagesimal('0;0,0,5'), Sexagesimal(whole=0, parts=[0,0,5]),
             'Multiple place __init__ fails with zeroes.'],

            #TODO: Allow for blank places
            #[Sexagesimal('0;,,5'), Sexagesimal(whole=0, parts=[0,0,5]),
            # 'Multiple place __init__ fails.'],

            [Sexagesimal('123123123123123123123'),
             Sexagesimal(whole=123123123123123123123, parts=[0]),
             'Large integer __init__ fails.'],

            [Sexagesimal('-0;15'), Sexagesimal('-0;15'), ''],

            #TODO: Allow Sexagesimal numbers to be created from negative floats
            #[Sexagesimal('-0;15'), Sexagesimal(-0.25), 'Fails on negative floats.'],
            #[Sexagesimal('-0;15'), Sexagesimal('-0.25'), 'Fails on negative floats as strings.'],

            #TODO: Allow Sexagesimal numbers to be created from unary floats
            #[Sexagesimal('crd1.0'), Sexagesimal(whole=1, parts=[0], unary='crd'),
            # 'Unary assignment fails with floats.']

            [Sexagesimal('-0;15'), Sexagesimal(whole=0, parts=[15], negative=True), ''],

            [Sexagesimal('crd1;0'), Sexagesimal('crd1;0'), ''],
            [Sexagesimal('crd1;0'), Sexagesimal(whole=1, parts=[0], unary='crd'),
             'Unary assignment fails.'],

        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_to_html(self):
        self.assertEqual(Sexagesimal('3;45').to_html(), Markup('3;45'))
        self.assertEqual(Sexagesimal('crd3;45').to_html(), Markup('<small>crd</small>(3;45)'))

    def test_has_unary(self):
        self.assertTrue(Sexagesimal('crd3;12').has_unary)
        self.assertFalse(Sexagesimal('3;12').has_unary)

    def test_addition(self):
        self.assertEqual(Sexagesimal('3;15') + Sexagesimal('2;20'),
                        Sexagesimal('5;35'))

        self.assertEqual(Sexagesimal('3;0') + Sexagesimal('2;0'),
                        Sexagesimal('5;0'))

        self.assertEqual(Sexagesimal('3;15') + Sexagesimal('2;45'),
                        Sexagesimal('6'))

    def test_multiplication(self):
        self.assertEqual(Sexagesimal('1;0') * Sexagesimal('1;0'),
                         Sexagesimal('1;0'),
                         '1;0 * 1;0 =? 1;0')

        self.assertEqual(Sexagesimal('-1;0') * Sexagesimal('1;0'),
                         Sexagesimal('-1;0'),
                         '-1;0 * 1;0 =? -1;0')


        self.assertEqual(Sexagesimal('1;0') * Sexagesimal('2;0'),
                         Sexagesimal('2;0'),
                         '1;0 * 2;0 =? 2;0')

        self.assertEqual(Sexagesimal('-1;0') * Sexagesimal('-2;0'),
                         Sexagesimal('2;0'))

        self.assertEqual(Sexagesimal('1;15') * Sexagesimal('2;0'),
                         Sexagesimal('2;30'),
                         '1;15 * 2;0 =? 2;30')

        self.assertEqual(Sexagesimal('1;0') * Sexagesimal('1;0'),
                         Sexagesimal('1;0'))

        self.assertEqual(Sexagesimal('1;0') * Sexagesimal('1;0'),
                         Sexagesimal('1;0'))

    def test_match(self):
        a = Sexagesimal('1;2,3,2')
        b = Sexagesimal('2;0')
        a.match(b)

        # Make sure that match has not actually changed the values
        self.assertEqual(a, Sexagesimal('1;2,3,2'))
        self.assertEqual(b, Sexagesimal('2;0'))

    def test_evaluate_unary(self):
        #self.fail()
        pass

    def test_whole(self):
        a = Sexagesimal('3;12')
        self.assertEqual(a.whole, 3)

        a = Sexagesimal('0;12')
        self.assertEqual(a.whole, 0)

        a = Sexagesimal(0.2)
        self.assertEqual(a.whole, 0)

        a = Sexagesimal(1.1)
        self.assertEqual(a.whole, 1)

    def test_parts(self):
        a = Sexagesimal('1;1,2,3')
        self.assertEqual(a.parts, [1,2,3])

        a = Sexagesimal('1;1,0,3')
        self.assertEqual(a.parts, [1,0,3])

        a = Sexagesimal(1.1)
        self.assertEqual(a.parts, [6])