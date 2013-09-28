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

@app.route('/query/', methods=['GET'])
@app.route('/')
def ptolemy():
	return render_template('pt.html', title="Ptolemy", instructions=True)

@app.route('/query/', methods=['POST'])
def evaluate_query():
	error = ''; steps = []; result = ''

	if request.method == 'POST':
		query = request.form['query']
		query = re.sub(r'\/','\:', query)
		query = re.sub(r'[^\w\*\+\-\/\:\^\;\,\.]', '', query)
		raw_parts = re.split('([\*\+\-\:\^])', query)	
		formatted_query = format_parts(raw_parts)
		if (raw_parts == ['']):
			error = "That query is not a query at all!"

	parts = []
	for x in raw_parts:
		if (";" in str(x) or "." in str(x)):
			try:
				parts.append(Sexagesimal(x))
			except Exception as e:
				error = e
				return render_template('pt.html', result=result, error=Markup(error))
		else:
			parts.append(x)
	
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
			subResult = Sexagesimal('').evaluate(parts[0], parts[2], parts[1])
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

def print_list(listy):
	html = "<ul>"
	for x in listy:
		html += '<li>%s</li>' % x
	html += '</ul>'
	return html