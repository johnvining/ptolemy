import string, math, sys, re
from flask import Markup

max_places = 3

from utils import Logger
l = Logger('sexa')

class Expression:
	def __init__(self, pieces):
		self.pieces = pieces
		self.unary = None

	@classmethod
	def from_string(cls, query):
		# convert string to list of strings
		l.l('New Expression from String: ' + str(query))

		error = ''
		query = re.sub(r'\/',':', query)
		re_only_alphanumeric_and_operators = re.compile(r'[^\w\*\+\-\/\:\^\;\,\.]')
		if re_only_alphanumeric_and_operators.search(query) is not None:
			error = "There was a problem with the query: " + str(query) + "<br/><small><small>This query contains characters that are not letters, numbers or operators.</small></small>"
		
		operators_as_strings = re.compile(r'[\*\+\-\:\^]')
		q = ''; z_l = ''
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

		raw_query_expression = re.split('([\*\+\-\:\^])', query)
		q = []; sub_expression = ''; level = 0
		for z in raw_query_expression:
			if '(' in str(z):
				if level == 0:
					sub_expression += z[1:]
				else:
					sub_expression += z
				level += 1
			elif ')' in str(z):
				level -= z.count(')')
				if level == 0:
					sub_expression += z[:-1]
					q.append(Expression.from_string(sub_expression))
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
		return cls(q)

	def to_html(self):
		html = ''; end_super = False
		for x in self.pieces:
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
			else:
				try:
					# Since the rest of `html` is a string and not a Markup
					# object, but to_html() returns an object, bring it back to
					# a string.
					html += str(x.to_html())
				except:
					html += str(x)
		return Markup(html)

	def __str__(self):
		s =''
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
					l.l('is instance: ' + str(s))
				else:
					s += str(x)
		return s

class Sexagesimal:

# 	A number is made of:
# 	* negative: True or False
# 	* unary: an attached unary operator like crd or sin or tan or sqrt
# 	* whole: the whole-number portion of the number, stored as integer
# 	* parts: the parts of '1;30,15' are [30,15], stored as a list of integers
	def __init__(self, s):
		l.v("Create a Sexagesimal from: " + str(s))
		# Given a Sexagesimal Number as String
		try:
			# If you can, change any ~ to -. If it doesn't work,
			#  it's problably a float.
			s = re.sub(r'\~','-', s)
		except Exception, e:
			pass
		
		# Decide if there is a unary operator attached
		if 'crd' in str(s):
			self.unary = 'crd'
			s = re.sub(r'[a-zA-Z]+','', s)
		else:
			self.unary = None

		if (';' in str(s)):
			whole_and_frac = string.split(s, ";")
			if ('-' not in str(whole_and_frac[0])):
				self.negative = False
			else:
				self.negative = True

			self.whole = abs(int(whole_and_frac[0]))
			
			if (',' in str(whole_and_frac[1])):
				fracs = string.split(whole_and_frac[1], ",")
				y = 1
				self.parts = []
				for x in fracs:
					self.parts.extend([int(x)])
			else:
				self.parts = [int(whole_and_frac[1])]

		# Given a Decimal Number _as string_
		elif ('.' in str(s)):
			if (float(s) >= 0):
				self.negative = False
			else:
				self.negative = True 
			
			i, d = divmod(float(s), 1)
			self.whole = abs(int(i))
			
			self.parts = []
			p = ''
			x = 0
			while (x < 3):
				i,d = divmod(d * 60, 1)
				self.parts.extend([int(i)])
				if (d * 60 < 1):
					break

		# Is it a whole number, garbage?
		else:
			# Trying to see if it's a whole number
			try:
				if (int(s) >= 0):
					self.negative = False
				else:
					self.negative = True
				self.whole = abs(int(s))
				self.parts = [0]

			# Apparently not a whole number
			except Exception as e:	
				raise Exception('Cannot Sexagesimalize \'' + str(s) + '\'<br/><small>' + str(e) + "</small>")

	def as_decimal(self):
		number_in_decimal = self.whole
		fracs = self.parts
		y = 1
		for x in fracs:
			x = float(x)
			denom = pow(60, y)
			number_in_decimal += x/denom
			y += 1

		if (self.negative):
			number_in_decimal = number_in_decimal * -1

		return number_in_decimal

	def de_unarize(self):
		a = self
		if self.unary == 'crd':
			result = 2 * math.sin(math.radians(self.as_decimal()/2))			
			try: 
				a = Sexagesimal(result)
			except Exception as e:
				l.e("There was an error: " + str(e))
				raise Exception(str(e))
		return a

	def has_unary(self):
		if self.unary is not None:
			return True
		else:
			return False

	def trim(self, places):
		if (len(self.parts) > places):
			self.parts = self.parts[0:places]
		return self

	def __str__(self):
		s = ''
		self.trim(max_places)
		if (self.negative == False):
			s += ''
		elif (self.negative == True):
			s += '-'

		s  += str(self.whole) + ";"
		places = len(self.parts)
		for x in self.parts:
			if (places > 1):
				s += str(x) + ","
			elif (places == 1):
				s += str(x)
			places -= 1

		if self.unary == 'crd':
			s = "crd(" + s + ")"
		
		return s

	# TODO: Rewrite this function to rely on __str__ above
	def to_html(self):
		s = ''
		self.trim(max_places)
		if (self.negative == False):
			s += ''
		elif (self.negative == True):
			s += '-'

		s  += str(self.whole) + ";"
		places = len(self.parts)
		for x in self.parts:
			if (places > 1):
				s += str(x) + ","
			elif (places == 1):
				s += str(x)
			places -= 1

		if self.unary == 'crd':
			s = "<small>crd</small>(" + s + ")"
		# Returns a Markup Object
		return Markup(s)

	def __neg__(self):
		a = Sexagesimal(str(self)) # TODO: Better way to copy?
		if (self.negative == True):
			a.negative = False
		elif (self.negative == False):
			a.negative = True
		else:
			a.negative = True
		return a

	def __abs__(self):
		a = Sexagesimal(str(self)) # TODO: Better way to copy?
		a.negative = False
		return a	

	def __add__(self, b):
		a = self
		
		# Is this actually a subtraction problem?
		if (a.negative == True and b.negative == True):
			return -(abs(a) + abs(b))
		elif (a.negative == True):
			return b - abs(a)
		elif (b.negative == True):
			return abs(a) - abs(b)
		else:
			a = self
			places = max(len(a.parts), len(b.parts))
			y = '0'
			for x in range(1, places): y += ',0' 
			result = Sexagesimal('0;' + y)

			c = 1; carry = 0
			while (c <= places):
				x = carry; carry = 0
				if (len(a.parts) > places - c): x += a.parts[places-c]
				if (len(b.parts) > places - c): x += b.parts[places-c]
				if (x >= 60): carry, x = divmod(x, 60)
				result.parts[places-c] = x
				c += 1
			result.whole = a.whole + b.whole + carry
			return result

	def __sub__(self, b):
		a = self

		if (a.negative == True and b.negative == True):
			return abs(b)-abs(a)
		elif (a.negative == True):
			return - (abs(a) + abs(b))
		elif (b.negative == True):
			return abs(a) + abs(b)
		elif (b.as_decimal() > a.as_decimal()):
			return - (b - a)
		else:
			places = max(len(a.parts), len(b.parts))
			# Create a Blank Result
			y = '0'
			for x in range(1, places): y += ',0' 
			result = Sexagesimal('0;' + y)

			c = places - 1; carry = 0
			while (c >= 0):
				x = carry; carry = 0
				if (len(a.parts) > c):
					x += a.parts[c]
						
				if (len(b.parts) > c):
					x -= b.parts[c]

				if (x < 0):
					x += 60
					carry = -1

				result.parts[c] = x
				c -= 1

			if (a.whole == b.whole and carry == -1):
				result.whole = 0
				result.negative = True
			else:
				result.whole = a.whole - b.whole + carry
			return result

	def __mul__(self, b):
		a = self
		return Sexagesimal(a.as_decimal() * b.as_decimal())

	def __div__(self, b):
		a = self
		return Sexagesimal(a.as_decimal() / b.as_decimal())

	def __pow__(self, b):
		a = self
		return Sexagesimal(a.as_decimal() ** b.as_decimal())

	def __cmp__(self, b):
		a = self.as_decimal()
		if type(b) != float and type(b) != int:
			b = b.as_decimal()

		if a > b:    return 1
		elif a == b: return 0
		elif a < b:  return -1

	def __eq__(self, b):
		if type(b) == unicode or type(b) == str:  return False
		elif type(b) == float or type(b) == int:  return self.as_decimal() == b
		elif self.as_decimal() == b.as_decimal(): return True