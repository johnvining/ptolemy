import string, math, sys, re
from flask import Markup
import copy

max_places = 90
base = 60

from utils import Logger, Error

l = Logger('sexa')


def as_n_d(whole, parts):
    n = base * whole
    d = 1
    for x in parts:
        d += 1
        n = (n + x) * base
    return n, d

def as_w_p(n, d):
    w, r = divmod(n, base ** d)
    c = d - 1
    p = []
    for x in range(c):
        part, r = divmod(r, base ** c)
        p.append(part)
        c -= 1
    return w, p

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
    def __init__(self, s=None, **kwargs):

        # Parse from a String
        if s is not None:
            # Replace ~ with -
            try:
                # If you can, change any ~ to -.
                s = re.sub(r'\~', '-', s)
            except:
                pass

            # Parse Unary
            if 'crd' in str(s):
                self.unary = 'crd'
                s = re.sub(r'[a-zA-Z]+', '', s)
            else:
                self.unary = None

            if (';' in str(s)):
                whole_and_frac = string.split(s, ";")
                if ('-' not in str(whole_and_frac[0])):
                    self.negative = False
                else:
                    self.negative = True

                whole = abs(int(whole_and_frac[0]))
                if (',' in str(whole_and_frac[1])):
                    fracs = string.split(whole_and_frac[1], ",")
                    y = 1
                    parts = []
                    for x in fracs:
                        parts.extend([int(x)])
                else:
                    parts = [int(whole_and_frac[1])]
                self.n, self.d = as_n_d(whole, parts)

            elif ('.' in str(s)):
                if (float(s) >= 0):
                    self.negative = False
                else:
                    self.negative = True

                i, r = divmod(float(s), 1)
                whole = abs(int(i))

                parts = []
                x = 0
                while True:
                    i, r = divmod(r * base, 1)
                    parts.extend([int(i)])
                    # TODO: Rewrite this to better decide
                    #  when to exist loop.
                    if (r * (base ** 3) < 0.01):
                        break
                self.n, self.d = as_n_d(whole, parts)

            # Is it a whole number, garbage?
            else:
                # Trying to see if it's a whole number
                try:
                    if (int(s) >= 0):
                        self.negative = False
                    else:
                        self.negative = True
                    whole = abs(int(s))
                    parts = [0]
                    self.n, self.d = as_n_d(whole, parts)
                # Apparently not a whole number
                except Exception as e:
                    raise Exception('Cannot Sexagesimalize \'' + str(s) + '\'<br/><small>' + str(e) + "</small>")

        # Get Variables Directly
        else:
            self.n = kwargs['n']
            self.d = kwargs['d']
            self.unary = None
            self.negative = False

    def __abs__(self):
        a = copy.deepcopy(self)
        a.negative = False
        return a

    def __cmp__(self, b):

        if isinstance(b, str):
            return -1
        a = copy.deepcopy(self)
        a.match(b)



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
        a = copy.deepcopy(self)
        return Sexagesimal(n=(a.n * b.n), d=(a.d + b.d))

    def __div__(self, b):
        a = copy.deepcopy(self)
        a.match(b)

        whole, remainder = divmod(a.n, b.n)
        c = 0
        parts = []
        while True:
            part, remainder = divmod(remainder * base, b.n)

            parts.append(part)
            c += 1
            if remainder == 0 or c > 5:
                break
        n,d = as_n_d(whole, parts)
        return Sexagesimal(n=n, d=d)

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
        if self.negative == True:
            s += '-'

        w, p = as_w_p(self.n, self.d)

        s += str(w) + ";"
        places = len(p)
        for x in p:
            if (places > 1):
                s += str(x) + ","
            elif (places == 1):
                s += str(x)
            places -= 1

        if self.unary == 'crd':
            s = "crd(" + s + ")"
        return s

    def __float__(self):
        return float(self.n) / (base ** self.d)

    def to_html(self):
        s = ''
        whole, parts = as_w_p(self.n, self.d)

        if (self.negative == False):
                s += ''
        elif (self.negative == True):
                s += '-'

        s += str(whole) + ";"
        places = len(parts)
        for x in parts:
                if (places > 1):
                        s += str(x) + ","
                elif (places == 1):
                        s += str(x)
                places -= 1

        if self.unary == 'crd':
                s = "<small>crd</small>(" + s + ")"
        # Returns a Markup Object
        return Markup(s)

    def has_unary(self):
        if self.unary is not None:
                return True
        else:
                return False

    def trim(self,x):
        # TODO: Write Trim Function
        return self

    def match(self, b):
        places = b.d
        if self.d < places:
            change = places - self.d
            self.n *= base ** change
            self.d += change
        elif self.d > places:
            b.match(self)

    def __pow__(self, b):
        # TODO: Write a specific method for whole number powers
        return Sexagesimal(self.as_decimal() ** b.as_decimal())

    def as_decimal(self):
        number_in_decimal, fracs = as_w_p(self.n, self.d)
        y = 1
        for x in fracs:
                x = float(x)
                denom = pow(60, y)
                number_in_decimal += x/denom
                y += 1

        if (self.negative):
                number_in_decimal = number_in_decimal * -1

        return number_in_decimal