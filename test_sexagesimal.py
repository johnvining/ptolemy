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

            [Sexagesimal('0;,,5'), Sexagesimal(whole=0, parts=[0,0,5]),
             'Multiple place __init__ fails.'],

            [Sexagesimal('123123123123123123123'),
             Sexagesimal(whole=123123123123123123123, parts=[0]),
             'Large integer __init__ fails.'],

            [Sexagesimal('-999999999;0,0,0,0,0,0,0,1'),
             Sexagesimal(whole=999999999, parts=[0, 0, 0, 0, 0, 0, 0, 1], negative=True),
             'Large integer __init__ fails.'],

            [Sexagesimal('-0;15'), Sexagesimal('-0;15'), ''],

            [Sexagesimal('-0;15'), Sexagesimal(-0.25), 'Fails on negative floats.'],
            [Sexagesimal('-0;15'), Sexagesimal('-0.25'), 'Fails on negative floats as strings.'],

            [Sexagesimal('crd1.0'), Sexagesimal(whole=1, parts=[0], unary='crd'),
            'Unary assignment fails with floats.'],

            [Sexagesimal('crd0.5'), Sexagesimal(whole=0, parts=[30], unary='crd'),
            'Unary assignment fails with floats.'],

            [Sexagesimal('-0;15'), Sexagesimal(whole=0, parts=[15], negative=True), ''],

            [Sexagesimal('crd1;0'), Sexagesimal('crd1;0'), ''],
            [Sexagesimal('crd1;0'), Sexagesimal(whole=1, parts=[0], unary='crd'),
             'Unary assignment fails.'],

        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_to_html(self):
        test_cases = [
            [Sexagesimal('3;45').to_html(),
             Markup('3;45'), ''],

            [Sexagesimal('crd3;45').to_html(),
             Markup('<small>crd</small>(3;45)'),
             'Sexagesimal with unary to_html fails.'],

            [Sexagesimal('-3;45').to_html(),
             Markup('-3;45'),
             'Negative Sexagesimal to_html fails.'],

            [Sexagesimal(5).to_html(), Markup('5;0'), ''],

            [(Sexagesimal('1;0') * Sexagesimal('2;0,0,0,0')).to_html(),
             Markup('2;0'), '']

        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_clean_up(self):
        test_cases = [
            ['2;0,0', '2;0', ''],
            ['2;2,2,2', '2;2,2,2', ''],
        ]

        for case in test_cases:
            self.assertEqual(Sexagesimal(case[0]).clean_up(), Sexagesimal(case[1]), case[2])


    def test_has_unary(self):
        self.assertTrue(Sexagesimal('crd3;12').has_unary)
        self.assertFalse(Sexagesimal('3;12').has_unary)

    def test_addition(self):
        test_cases = [
            [Sexagesimal('3;0') + Sexagesimal('2;0'),
             Sexagesimal('5;0'), ''],

            [Sexagesimal('3;15') + Sexagesimal('2;20'),
             Sexagesimal('5;35'), ''],

            [Sexagesimal('3;15') + Sexagesimal('2;45'),
             Sexagesimal('6'), ''],

            [Sexagesimal('0;30') + Sexagesimal('0;30'),
             Sexagesimal('1'), ''],

            [Sexagesimal('-0;30') + Sexagesimal('1'),
             Sexagesimal('0;30'), ''],

            [Sexagesimal('1;0') + Sexagesimal('-0;30'),
             Sexagesimal('0;30'), ''],

            [Sexagesimal('-1;30') + Sexagesimal('-3;15'),
             Sexagesimal('-4;45'), '']
        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_subtraction(self):
        test_cases = [
            [Sexagesimal('3;0') - Sexagesimal('2;0'),
             Sexagesimal('1;0'), ''],

            [Sexagesimal('3;0') - Sexagesimal('2;15'),
             Sexagesimal('0;45'), ''],

            [Sexagesimal('3;0') - Sexagesimal('-2;0'),
             Sexagesimal('5;0'), ''],

            [Sexagesimal('-3;0') - Sexagesimal('2;0'),
             Sexagesimal('-5;0'), ''],

            [Sexagesimal('-3;0') - Sexagesimal('-2;0'),
             Sexagesimal('-1;0'), ''],

            [Sexagesimal('3;5,5,5,5') - Sexagesimal('0;5,0,5,0'),
             Sexagesimal('3;0,5,0,5'), ''],
        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_multiplication(self):
        test_cases = [
            [Sexagesimal('1;0') * Sexagesimal('1;0'),
             Sexagesimal('1;0'), ''],

            [Sexagesimal('-1;0') * Sexagesimal('1;0'),
             Sexagesimal('1;0'), ''],

            [Sexagesimal('1;0') * Sexagesimal('1;0'),
             Sexagesimal('-1;0'), ''],

            [Sexagesimal('-1;0') * Sexagesimal('-1;0'),
             Sexagesimal('1;0'), ''],

            [Sexagesimal('1;15') * Sexagesimal('2;0'),
             Sexagesimal('2;30'), ''],

            [Sexagesimal('2;0') * Sexagesimal('1;15'),
             Sexagesimal('2;30'), ''],
        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_division(self):
        test_cases = [
            [Sexagesimal('3;50') / Sexagesimal(2),
             Sexagesimal('1;55'), ''],

            [Sexagesimal(2) / Sexagesimal(2),
            Sexagesimal(1), ''],

            [Sexagesimal('1;30') / Sexagesimal('0;30'),
            Sexagesimal('3;0'), ''],

            [Sexagesimal('0;0') / Sexagesimal('2;0'),
            Sexagesimal('0;0'), ''],

            [Sexagesimal('1;0') / Sexagesimal('1;0'),
            Sexagesimal('1;0'), ''],
        ]

        for case in test_cases:
            self.assertEqual(case[0], case[1], case[2])

    def test_match(self):
        test_cases = [
            ['1;2,3,2', '2;0', ''],
            ['9999999999999999999', '0;0,0,0,0,0,1',
             'Large integer and small Sexagesimal fails.']
        ]

        for case in test_cases:
            a = Sexagesimal(case[0])
            b = Sexagesimal(case[1])
            a.match(b)

            self.assertEqual(a, Sexagesimal(case[0]), case[2])
            self.assertEqual(b, Sexagesimal(case[1]), case[2])

    def test_evaluate_unary(self):
        #Write test cases for evaluate unary
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