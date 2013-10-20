import os, sys, string, re
from flask import Flask, url_for, render_template, request, Markup
from calculator import *
from sexagesimal import Expression
from utils import Logger

app = Flask(__name__)
app.debug = True

@app.route('/', methods = ['GET','POST'])
def evaluate_query():
	error = ''
	l = Logger()

	if request.method == 'GET':
		l.l('request.method = GET')
		# If there is no query, display the basic page with instructions
		return render_template('pt.html', instructions=False)
	
	elif request.method == 'POST':
		l.l('request.method = POST')
		# If method = Post, parse the query
		calc = Calculator()
		query_expression = Expression.from_string(request.form['query'])
		q_e_html = query_expression.to_html()
		
		# TODO: The following is destructive and should not be.
		result, steps = calc.evaluate_expression(query_expression)
		
		if (error==''): 
			return render_template('pt.html', steps=steps, query=q_e_html, result=str(result), warning='')
		else:
			return render_template('pt.html', result=result, error=Markup(error))




def create_alert(kind, text):
	html = '<div class="%s">%s</div>' % (kind, text)
	return html

def print_list(listy):
	html = "<ul>"
	for x in listy:
		html += '<li>%s</li>' % str(x)
	html += '</ul>'
	return html