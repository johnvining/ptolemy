import os, sys, string, re
from flask import Flask, url_for, render_template, request, Markup
from sexagesimal import *

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
	error = ''; steps = []; result = ''
	if request.method == 'GET':
		return render_template('pt.html', instructions=True)
	elif request.method == 'POST':
		parts, formatted_query, error = parse_query(request.form['query'])	
		if (error != ''):
			return render_template('pt.html', instructions=True, error=Markup(error))

		while True:
			
			try:
				if (len(parts) == 1):
					result = parts[0]
					break
				elif (len(parts) < 4):
					result = Sexagesimal('').evaluate(parts[0], parts[2], parts[1])
					break
				c = 0; triplets = []; length = len(parts) - 2	
				
				while (c < length):
					triplets.extend([parts[c:c+3]])
					c = c + 1
				d = next_to_evaluate(triplets)

				# TODO: Create a Ptolemy Calc Class
				subResult = Sexagesimal('').evaluate(parts[d], parts[d+2], parts[d+1])
				parts.pop(d); parts.pop(d+1)
				
				parts[d] = subResult
				steps.append(Markup(format_parts(parts)))
			except Exception as e:
				error = "There was a problem with the query: " + formatted_query + '<br/><small><small>Python sez: ' + str(e) + '</small></small>'
				break

		if (error==''): 
			return render_template('pt.html', steps=steps, result=Markup(result), query=Markup(formatted_query), warning=Markup(warning))
		else:
			return render_template('pt.html', result=result, error=Markup(error))

def next_to_evaluate(triplets):
	order = ['^', '*', ':', '+', '-']
	for operator in order:
		c = 0
		for x in triplets:		
			if (x[1] == operator):
				return c
			c += 1
	return 0


def parse_query(query):
	error = ''

	query = re.sub(r'\/','\:', query)
	re_only_alphanumeric_and_operators = re.compile(r'[^\w\*\+\-\/\:\^\;\,\.]')
	if re_only_alphanumeric_and_operators.search(query) is not None:
		error = "There was a problem with the query: " + str(query) + "<br/><small><small>This query contains characters that are not letters, numbers or operators.</small></small>"
	
	raw_parts = re.split('([\*\+\-\:\^])', query)

	if (raw_parts == ['']):
		error = "That query is not a query at all!"

	parts = []
	for x in raw_parts:
		try:
			parts.append(Sexagesimal(x))
		except:
			# Anything that cannot be sexagesimalized is considered
			# an operator.
			parts.append(x)

	return parts, format_parts(raw_parts), error

def format_parts(parts):
	html = ''; endSuper = False
	for x in parts:
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