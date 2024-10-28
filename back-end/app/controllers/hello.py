"""
    Example Controllers
"""
from flask import render_template, redirect, url_for
from flask import Blueprint

"""
    Import MOdels
from app.models.Hello import Hello
//Call HelloService
"""

index_blueprint = Blueprint('index', __name__)
# route index
@index_blueprint.route('/', methods = ['GET'])
def index():
    data = {
        "title": "Hello World",
        "body": "Flask simple MVC"
    }
    return render_template('index.html.j2', data = data)
