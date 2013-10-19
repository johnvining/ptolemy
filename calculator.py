import re
from sexagesimal import *
from flask import Markup

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

		raw_query_expression = re.split('([\*\+\-\:\^])', query)

		if (raw_query_expression == ['']):
			error = "That query is not a query at all!"

		# TODO: Remove hard-coded reference to Sexagesimal()
		query_expression = []
		for x in raw_query_expression:
			try:
				query_expression.append(Sexagesimal(x))
			except:
				# Anything that cannot be sexagesimalized is considered
				# an operator. This will change with unary operators.
				query_expression.append(x)

		return query_expression, error

	def evaluate_expression(self, expression):
		steps = []; error = ''; query_expression = expression.pieces; result = 100000

		# Check for expressions within the expression, evaluate those
		expression_list_copy = []; c = 0
		for x in query_expression:
			if isinstance(x, Expression):
				result_from_parenthetical, steps_for_parenthetical = self.evaluate_expression(x)
				expression_list_copy.append(result_from_parenthetical)
				beginning_string = Expression(query_expression[:c]).to_html()
				end_string = Expression(query_expression[c+1:]).to_html()
				steps.append(Markup(beginning_string+"("+x.to_html()+")"+end_string))

				for y in steps_for_parenthetical:
					steps.append(Markup(beginning_string + "(" + Expression(y).to_html() + ")" + end_string))
			else:
				expression_list_copy.append(x)
			c += 1	
		query_expression = expression_list_copy


		# TODO: Check for Unaries, evaluate those
		
		# General order of operations
		continuey = True
		while continuey:
			try:
				if (len(query_expression) == 1):
					# If the query is a single number 
					result = query_expression[0]
					continuey = False
				elif (len(query_expression) == 3):
					# If the query has been solved down the last triplet, evaluate and set result
					result = self.evaluate(query_expression[0], query_expression[2], query_expression[1])
					continuey = False
				else:
					c = 0; triplets = []; length = len(query_expression) - 2
					while (c < length):
						triplets.extend([query_expression[c:c+3]])
						c = c + 1
					d = self.next_to_evaluate(triplets)
					sub_result = self.evaluate(query_expression[d], query_expression[d+2], query_expression[d+1])
					query_expression.pop(d); query_expression.pop(d+1)
					query_expression[d] = sub_result
					try:
						steps.append(Markup(Expression(query_expression).to_html()))
					except Exception as e:
						pass
			except Exception as e:
				try:
					error += '<span class="expression"><center>' + formatted_query + '</center></span><br/>'
					print error; sys.stdout.flush()
				except Exception as e_1:
					error += str(e_1) + "<br/><br/>"
					error += "There was a problem with the query. Python sez: " + str(e)
					print error; sys.stdout.flush()
					continuey = False
				continuey = False

		return result, steps


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

	def evaluate(self, a, b, operator):
		if (operator == "*"): return (a * b).trim(self.trim)
		elif (operator == "+"): return (a + b).trim(self.trim)
		elif (operator == ':'): return (a / b).trim(self.trim)
		elif (operator == '-'): return (a - b).trim(self.trim)
		elif (operator == '^'): return (a ** b).trim(self.trim)
		else:
			raise Exception(str(operator) + ' is not a valid operator.')