import re
from sexagesimal import *

class Calculator:
	def __init__(self, order_of_operations='PEMDAS', trim=6):
		if order_of_operations == 'PEMDAS':
			self.order_of_operations = 'PEMDAS'
		elif order_of_operations == 'LEFT TO RIGHT':
			self.order_of_operations = 'LEFT TO RIGHT'
		self.trim = trim

	def parse_query(self, query):
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

		raw_query_list = re.split('([\*\+\-\:\^])', query)

		if (raw_query_list == ['']):
			error = "That query is not a query at all!"

		# TODO: Remove hard-coded reference to Sexagesimal()
		query_list = []
		for x in raw_query_list:
			try:
				query_list.append(Sexagesimal(x))
			except:
				# Anything that cannot be sexagesimalized is considered
				# an operator. This will change with unary operators.
				print "could not sexagesimalize" + str(x); sys.stdout.flush()
				query_list.append(x)

		return query_list, error

	def next_to_evaluate(self, triplets):
		if self.order_of_operations == 'PEMDAS':
			order = ['^', '*', ':', '+', '-']
			for operator in order:
				c = 0
				for x in triplets:		
					if (x[1] == operator):
						return c
					c += 1
			return 0
		elif self.order_of_operations == 'LEFT TO RIGHT':
			return 0

		# Move Evaluate to Main Calculator Section
	def evaluate(self, a, b, operator):
		if (operator == "*"): return (a * b).trim(self.trim)
		elif (operator == "+"): return (a + b).trim(self.trim)
		elif (operator == ':'): return (a / b).trim(self.trim)
		elif (operator == '-'): return (a - b).trim(self.trim)
		elif (operator == '^'): return (a ** b).trim(self.trim)
		else:
			raise Exception(str(operator) + ' is not a valid operator.')