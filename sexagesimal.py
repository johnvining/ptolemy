import string, math

class Sexagesimal:
	def __init__(self, s): 
		if (';' in str(s)):
			self.base = 60
			whole_and_frac = string.split(s, ";")
			self.whole = int(whole_and_frac[0])
			if (',' in str(whole_and_frac[1])):
				fracs = string.split(whole_and_frac[1], ",")
				y = 1
				self.parts = []
				for x in fracs:
					self.parts.extend([int(x)])
			else:
				self.parts = [int(whole_and_frac[1])]
		elif ('.' in str(s)):
			self.base = 10
			self.decfloat = float(s)
		else:
			self.whole = int(s)


	def __str__(self):
		if (self.base == 60):
			s  = str(self.whole) + ";"
			places = len(self.parts)
			for x in self.parts:
				if (places > 1):
					s += str(x) + ","
				elif (places == 1):
					s += str(x)
				places -= 1
			return s
		elif (self.base == 10):
			return str(self.decfloat)
	
	def evaluate(a, b, operator)
		if (operator == "*"):
			return Sexagesimal(decimal(x) * decimal(y))
		elif (operator == "+"):
			return self.add(a, b)
		elif (operator == ':'):
			return Sexagesimal(decimal(x) / decimal(y))
		elif (operator == '-'):
			return self.subtract(a, b)
		elif (operator == '^'):
			return Sexagesimal(decimal(x) ** decimal(y))
		else:
			return 1000 #For debugging purposes

	def add(a, b):
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

	def subtract(a, b):
		places = max(len(a.parts), len(b.parts))
		y = '0'
		for x in range(1, places): y += ',0' 
		result = Sexagesimal('0;' + y)

		c = 1; carry = 0
		while (c <= places):
			x = carry; carry = 0
			if (len(a.parts) > places - c): x += a.parts[places-c]
			else: x = 0 + carry
			if (len(b.parts) > places - c): x -= b.parts[places-c]
			if (x < 0): x += 60; carry = -1
			result.parts[places-c] = x
			c += 1

		result.whole = a.whole + b.whole + carry
		return result

a = Sexagesimal('2;0')
b = Sexagesimal('0;15,15')
print Sexagesimal.subtract(a, b)



