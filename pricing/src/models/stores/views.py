from flask import Blueprint

store_blueprint = Blueprint(name='stores', import_name='__name__')


@store_blueprint.route('/')
def index():
    return "This is the stores index page"


@store_blueprint.route('/store/<string:name>')
def store_page(name: str):
    pass
