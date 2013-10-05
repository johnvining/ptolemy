import string, math, sys, re

# TODO: Move this somewhere better:
max_places = 6

class Sexagesimal:

# 	A number is made of:
# 	* negative: True or False
# 	* whole: the whole-number portion of the number, stored as integer
# 	* parts: the parts of '1;30,15' are [30,15], stored as a list of integers
	def __init__(self, s): 
		# Given a Sexagesimal Number as String
		s = re.sub(r'\~','-', s)

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

		# Given a Decimal Number
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

		elif( s == ''):
			pass

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



	def to_decimal(self):
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

	# Move Evaluate to Main Calculator Section
	def evaluate(self, a, b, operator):
		if (operator == "*"): return a * b
		elif (operator == "+"): return a + b
		elif (operator == ':'): return a / b
		elif (operator == '-'): return a - b
		elif (operator == '^'): return a ** b
		else:
			raise Exception(str(operator) + ' is not a valid operator.')

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

	def __str__(self):
		s = ''
		self.trim(max_places)
		if (self.negative == False):
			s += ''
		elif (self.negative == True):
			s += '-'
		else:
			s += '!uns!'

		s  += str(self.whole) + ";"
		places = len(self.parts)
		for x in self.parts:
			if (places > 1):
				s += str(x) + ","
			elif (places == 1):
				s += str(x)
			places -= 1
		return s	
	
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
		elif (b.to_decimal() > a.to_decimal()):
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
		result = a.to_decimal() * b.to_decimal()
		result = Sexagesimal(str(result))
		return result

	def __div__(self, b):
		a = self
		result = a.to_decimal() / b.to_decimal()
		result = Sexagesimal(str(result))
		return result

	def __pow__(self, b):
		a = self
		result = a.to_decimal() ** b.to_decimal()
		result = Sexagesimal(str(result))
		return result

	## TODO: Overwrite the comparison operators and replace usage of to_deciamal in comparators

	def trim(self, places):
		if (len(self.parts) > places):
			self.parts = self.parts[0:places]
		return self