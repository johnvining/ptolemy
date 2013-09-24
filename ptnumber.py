# class Number:
# 	def __init__(self, s): 
# 		if (';' in str(s)):
# 			self.base = 60
# 			whole_and_frac = string.split(s, ";")
# 			self.whole = int(whole_and_frac[0])
# 			if (',' in str(whole_and_frac[1])):
# 				fracs = string.split(whole_and_frac[1], ",")
# 				y = 1
# 				self.parts = []
# 				for x in fracs:
# 					self.parts.extend([int(x)])
# 			else:
# 				self.parts = [int(whole_and_frac[1])]
# 		elif ('.' in str(s)):
# 			self.base = 10
# 			self.decfloat = float(s)
# 		else:
# 			self.whole = int(s)


# 	def print_number(self, places=4):
# 		if (self.base == 60):
# 			s  = str(self.whole) + ";"
# 			places = min(places, len(self.parts))
# 			for x in self.parts:
# 				if (places > 1):
# 					s += str(x) + ","
# 				elif (places == 1):
# 					s += str(x)
# 				places -= 1
# 		elif (self.base == 10):
# 			s = str(self.decfloat)

# 		return s

# 	# TODO: Switch to: Print natural (b60 or b10 based on number), and specific
# 	# methods to force the conversion.