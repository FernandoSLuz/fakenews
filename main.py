import sys
import os
import time

import flask
import requests

from wassengerBackend import blueprint as wassengerBackend_blueprint
from dialogflowBackend import blueprint as dialogflowBackend_blueprint

app = flask.Flask(__name__)

app.secret_key = 'secret'

app.register_blueprint(wassengerBackend_blueprint)
app.register_blueprint(dialogflowBackend_blueprint)


@app.route('/')
def index():
    context = {
        'title':'Hacka | Olivetti'
    }
    return (context)

if __name__ == "__main__":
    root_module = os.path.abspath(os.path.curdir)
    sys.path.append(root_module)
    app.run(host='0.0.0.0')