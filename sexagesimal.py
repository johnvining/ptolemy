import string, re
from flask import Markup
import copy
import math

max_places = 90
base = 60

from utils import Logger, Error

l = Logger('sexa')


class Expression:
    def __init__(self, pieces):
        self.pieces = pieces
        self.unary = None

    @classmethod
    def from_string(cls, query):
        # convert string to list of strings
        l.l('New Expression from String: ' + str(query))

        errors = []
        query = query.replace(" ", "")
        query = re.sub(r'\/', ':', query)
        re_only_alphanumeric_and_operators = re.compile(r'[^\w\*\+\-/:\^;,\.\(\)]')
        if re_only_alphanumeric_and_operators.search(query) is not None:
            errors.append(
                Error('This query contains characters that are not letters, numbers or operators.', query, None))

        operators_as_strings = re.compile(r'[\*\+\-\:\^]')
        q = '';
        z_l = ''
        for z in query:
            # IF it's a minus sign AND
            #  It's the first character OR
            #  It comes after another operator
            # THEN: Replace w/ ~

            if z == "-" and (operators_as_strings.search(z_l) is not None or z_l == ''):
                q += "~"
            else:
                q += z
            z_l = z
        query = q

        raw_query_expression = re.split(r'([\*\+\-:\^])', query)
        q = []
        sub_expression = ''
        level = 0
        for z in raw_query_expression:
            if '(' in str(z) and ')' in str(z) and level == 0:
                y = z.replace("(", "")
                y = y.replace(")", "")
                q.append(Sexagesimal(y))
            elif '(' in str(z):
                if level == 0:
                    sub_expression += z[1:]
                else:
                    sub_expression += z
                level += 1
            elif ')' in str(z):
                level -= z.count(')')
                if level == 0:
                    sub_expression += z[:-1]
                    expr, ignore = Expression.from_string(sub_expression)
                    q.append(expr)
                    sub_expression = ''
                else:
                    sub_expression += z
            elif level != 0:
                sub_expression += z
            else:
                try:
                    q.append(Sexagesimal(z))
                except Exception as e:
                    # Anything that cannot be sexagesimalized is considered
                    # an operator.
                    q.append(z)
                    l.v('Could not sexagesimalize ' + str(z))

        if level != 0:
            errors.append(Error('Please close all parentheses!', None, None))
            level = 0

        return cls(q), errors

    def to_html(self):
        html = ''
        end_super = False
        for x in self.pieces:
            if isinstance(x, basestring):
                if (x == '^'):
                    html += '<sup>'
                    end_super = True
                elif (end_super):
                    html += str(x) + '</sup>'
                    end_super = False
                elif (x == '+'):
                    html += ' <b>+</b> '
                elif (x == '*'):
                    html += ' &times; '
                elif (x == ':'):
                    html += ' <b>:</b> '
                elif (x == '-'):
                    html += ' <b>&ndash;</b> '
            elif isinstance(x, Expression):
                # Since the rest of `html` is a string and not a Markup
                # object, but to_html() returns an object, bring it back to
                # a string.
                html += '(' + str(x.to_html()) + ')'
            elif isinstance(x, Sexagesimal):
                html += str(x.to_html())
            else:
                html += str(x)

        return Markup(html)

    def __str__(self):
        s = ''
        for x in self.pieces:
            if (x == '^'):
                s += '^'
            elif (x == '+'):
                s += ' + '
            elif (x == '*'):
                s += ' * '
            elif (x == ':'):
                s += ' : '
            elif (x == '-'):
                s += ' - '
            else:
                if isinstance(x, Expression):
                    s += '(' + str(x) + ')'
                else:
                    s += str(x)
        return s


class Sexagesimal:
    def __init__(self, s=None, unary=None, negative=False, **kwargs):
        if 'n' in kwargs:
            self.n = kwargs['n']
            self.unary = unary
            self.negative = negative
            if 'd' in kwargs:
                self.d = kwargs['d']
            else:
                # TODO Write Error function for 'n' but no 'd'
                pass
        # Create number from whole/parts
        elif 'whole' in kwargs:
            whole = kwargs['whole']
            parts = kwargs['parts']
            n = base * whole
            d = 1
            for x in parts:
                d += 1
                n = (n + x) * base
            self.n = n
            self.d = d
            self.unary = unary
            self.negative = negative

        elif '.' in str(s):
            if float(s) < 0:
                negative = True

            s = abs(float(s))

            whole, r = divmod(float(s), 1)

            parts = []
            while True:
                i, r = divmod(r * base, 1)
                parts.extend([int(i)])
                # TODO: Rewrite this to better decide
                #  when to exit loop.
                if r * (base ** 3) < 0.01:
                    break

            self.__init__(whole=whole,
                          parts=parts,
                          unary=unary,
                          negative=negative)

        # Parse from a String
        else:
            self.parse_from_string(s)

    def parse_from_string(self, s):
        # Replace ~ with -
        try:
            # If you can, change any ~ to -.
            s = re.sub(r'~', '-', str(s))
        except Exception as e:
            pass

        if '-' in str(s):
            negative = True
        else:
            negative = False
        s = re.sub(r'\-', '', s)

        # Parse Unary
        unary = None
        if 'crd' in str(s):
            unary = 'crd'
            s = re.sub(r'[a-zA-Z]+', '', s)

        if ';' in str(s):
            whole_and_frac = string.split(s, ';')
            whole = int(whole_and_frac[0])
            if ',' in str(whole_and_frac[1]):
                fracs = string.split(whole_and_frac[1], ',')
                parts = []
                for x in fracs:
                    if x is '':
                        parts.append(0)
                    else:
                        parts.append(int(x))
            else:
                parts = [int(whole_and_frac[1])]

            self.__init__(whole=whole,
                          parts=parts,
                          unary=unary,
                          negative=negative)

        # Is it a whole number or garbage?
        else:
            # Trying to see if it's a whole number
            try:
                self.__init__(whole=int(s),
                              parts=[0],
                              unary=unary,
                              negative=negative)

            #Apparently not a whole number
            except Exception as e:
                raise Exception('Cannot Sexagesimalize ' + str(s))

    def __abs__(self):
        a = copy.deepcopy(self)
        a.negative = False
        return a

    def __cmp__(self, b):

        if isinstance(b, str):
            return -1
        a = copy.deepcopy(self)
        a.match(b)

        # TODO: Add support for negatives
        if a.n > b.n:
            return 1
        elif a.n == b.n:
            return 0
        elif a.n < b.n:
            return -1

    def __add__(self, b):
        a = copy.deepcopy(self)

        # Is this actually a subtraction problem?
        if (a.negative == True and b.negative == True):
            return -(abs(a) + abs(b))
        elif (a.negative == True):
            return b - abs(a)
        elif (b.negative == True):
            return abs(a) - abs(b)
        else:
            a.match(b)
            return Sexagesimal(n=(a.n + b.n), d=a.d)

    def __mul__(self, b):
        negative = False
        if self.negative and b.negative is False:
            negative = True
        elif b.negative and self.negative is False:
            negative = True

        return Sexagesimal(n=(self.n * b.n), d=(self.d + b.d), negative=negative)

    def __div__(self, b):
        a = copy.deepcopy(self)
        a.match(b)

        negative = False
        if a.negative and not b.negative:
            negative = True
        elif b.negative and not a.negative:
            negative = True

        whole, remainder = divmod(a.n, b.n)
        c = 0
        parts = []
        while True:
            part, remainder = divmod(remainder * base, b.n)

            parts.append(part)
            c += 1
            if remainder == 0 or c > 5:
                break
        return Sexagesimal(whole=whole, parts=parts, negative=negative)

    def __sub__(self, b):
        a = copy.deepcopy(self)

        if (a.negative == True and b.negative == True):
            return abs(b) - abs(a)
        elif (a.negative == True):
            return - (abs(a) + abs(b))
        elif (b.negative == True):
            return abs(a) + abs(b)
        elif (b > a):
            return - (b - a)
        else:
            a.match(b)
            return Sexagesimal(n=(a.n - b.n), d=a.d)

    def __neg__(self):
        a = copy.deepcopy(self)
        if (self.negative == True):
            a.negative = False
        elif (self.negative == False):
            a.negative = True
        else:
            a.negative = True
        return a

    def __str__(self):
        s = ''
        if self.negative:
            s += '-'

        w = self.whole
        p = self.parts

        s += str(w) + ";"
        places = len(p)
        for x in p:
            if places > 1:
                s += str(x) + ","
            elif places == 1:
                s += str(x)
            places -= 1

        if self.unary == 'crd':
            s = "crd(" + s + ")"
        return s

    def __float__(self):
        if self.unary is not None:
            return float(self.evaluate_unary())
        elif self.negative:
            return float(self.n * -1) / (base ** self.d)
        else:
            return float(self.n) / (base ** self.d)


    def to_html(self, max_places=6):
        s = ''

        if self.negative:
            s += '-'

        s += str(self.whole) + ";"
        places = min(len(self.parts), max_places)
        for x in self.parts:
            if places > 1:
                s += str(x) + ","
            elif places == 1:
                s += str(x)
            places -= 1

        if self.unary == 'crd':
            s = "<small>crd</small>(" + s + ")"
            # Returns a Markup Object
        return Markup(s)

    @property
    def has_unary(self):
        if self.unary is not None:
            return True
        else:
            return False

    def match(self, b):
        places = b.d
        if self.d < places:
            change = places - self.d
            self.n *= base ** change
            self.d += change
        elif self.d > places:
            b.match(self)

    def evaluate_unary(self):
        if self.unary == 'crd':
                self.unary = None

                result = 2 * math.sin(math.radians(float(self)/2))
                try:
                    self.__init__(result)
                except Exception as e:
                    l.e("There was an error: " + str(e))
                    raise Exception(str(e))
        return self

    def __pow__(self, b):
        a = copy.deepcopy(self)
        original_a = copy.deepcopy(self)
        if b.parts == [0]:
            print 'b.whole:', b.whole
            for x in range(b.whole - 1):
                a *= original_a
            return a

        else:
            print 'floaty',a,b,
            return Sexagesimal(float(self) ** float(b))

    @property
    def whole(self):
        whole, r = divmod(self.n, base ** self.d)
        return whole

    @property
    def parts(self):
        whole, r = divmod(self.n, base ** self.d)
        c = self.d - 1
        parts = []
        for x in range(c):
            part, r = divmod(r, base ** c)
            parts.append(part)
            c -= 1
        return parts

    def clean_up(self):
        while self.n % base == 0:
            self.n /= base
            self.d -= 1

        return self