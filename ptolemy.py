import os, sys, string, re
from flask import Flask, url_for, render_template, request, Markup
from sexagesimal import *
from calculator import *

app = Flask(__name__)
app.debug = True

warning = '''
			<small>Multiplication and division calculations are
			conducted by first converting the number to decimal, performing
			the multiplcation and converting back. This is not completely
			accurate. All numbers are trimed at six places.</small>
		  '''

@app.route('/', methods = ['GET','POST'])
def evaluate_query():
	error = ''

	if request.method == 'GET':
		# If there is no query, display the basic page with instructions
		return render_template('pt.html', instructions=True)
	
	elif request.method == 'POST':
		# If method = Post, parse the query
		calc = Calculator()
		query_list, error = calc.parse_query(request.form['query'])	
		formatted_query = format_query_list(query_list)
		if (error != ''):
			# If there is an error with parsing, stop, and return an error page.
			return render_template('pt.html', instructions=True, error=Markup(error))

		
		steps = []; result = ''
		while True:	
			try:
				if (len(query_list) == 1):
					# If the query is a single number 
					result = query_list[0]
					break
				elif (len(query_list) == 3):
					# If the query has been solved down the last triplet, evaluate and set result
					result = calc.evaluate(query_list[0], query_list[2], query_list[1])
					break

				# If neither of the above catches, we need to 
				#  do the next step in the calculation
				
				# Split into triplets and pick the next triplet to
				#  evaluate based on order of operations
				#
				# A triplet looks like: [2;3, '*', 1;0]; the numbers
				#  are stored as Sexagesimal objects.
				c = 0; triplets = []; length = len(query_list) - 2
				while (c < length):
					triplets.extend([query_list[c:c+3]])
					c = c + 1
				d = calc.next_to_evaluate(triplets)

				# Evaluate this triplet and insert answer into first
				#  spot in list, pop out the other two query_list in query_list
				sub_result = calc.evaluate(query_list[d], query_list[d+2], query_list[d+1])
				query_list.pop(d); query_list.pop(d+1)
				query_list[d] = sub_result

				# Append the HTML for this step to steps
				steps.append(Markup(format_query_list(query_list)))
			except Exception as e:
				error = "There was a problem with the query: " + formatted_query + '<br/><small><small>Python sez: ' + str(e) + '</small></small>'
				break

		if (error==''): 
			return render_template('pt.html', steps=steps, result=Markup(result), query=Markup(formatted_query), warning=Markup(warning))
		else:
			return render_template('pt.html', result=result, error=Markup(error))



def format_query_list(query_list):
	html = ''; endSuper = False
	for x in query_list:
		if (x == '^'):
			html += '<sup>'
			endSuper = True
		elif (endSuper):
			html += str(x) + '</sup>'
			endSuper = False
		elif (x == '+'):
			html += ' <b>+</b> '
		elif (x == '*'):
			html += ' &times; '
		elif (x == ':'):
			html += ' <b>:</b> '
		elif (x == '-'):
			html += ' <b>&ndash;</b> '
		else:
			html += str(x)
	return html

def create_alert(kind, text):
	html = '<div class="%s">%s</div>' % (kind, text)
	return html

def print_error(s):
	print s
	sys.stdout.flush()

def print_list(listy):
	html = "<ul>"
	for x in listy:
		html += '<li>%s</li>' % str(x)
	html += '</ul>'
	return html