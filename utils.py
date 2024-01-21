import sys
from markupsafe import Markup


class Logger:
    def __init__(self, location):
        self.location = location

    def l(self, message, importance='info'):
        if importance == 'error':
            print(self.location + " :ERROR: " + message, flush=True)
        elif importance == 'verbose':
            pass
        else:
            print(self.location + " :: " + message, flush=True)

    def e(self, message):
        self.l(message, importance='error')

    def v(self, message):
        self.l(message, importance='verbose')


class Error:
    def __init__(self, message, obj=None, python_error=None):
        self.message = message
        self.obj = obj
        self.python_error = python_error

    def to_html(self):
        html = ''
        html += self.message

        if self.obj is not None:
            html += '<br/><br/><center><span class="expression">'
            try:
                html += str(self.obj.to_html())
            except:
                try:
                    html += str(str(self.obj))
                except:
                    pass
            html += '</center></span>'

        if self.python_error is not None:
            html += '<br/><small>Python says: '
            html += str(self.python_error)
            html += '</small>'

        return Markup(html)