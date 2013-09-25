import string, math

class Pt_Number:
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


	def print_number(self, places=10):
		if (self.base == 60):
			s  = str(self.whole) + ";"
			places = min(places, len(self.parts))
			for x in self.parts:
				if (places > 1):
					s += str(x) + ","
				elif (places == 1):
					s += str(x)
				places -= 1
		elif (self.base == 10):
			s = str(self.decfloat)

		return s

	def pt_add(a, b):
		places = max(len(a.parts), len(b.parts))
		y = '0'
		for x in range(1, places): y += ',0' 
		result = Pt_Number('0;' + y)

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

a = Pt_Number('41;20')
b = Pt_Number('22;40')
print Pt_Number.pt_add(a, b)