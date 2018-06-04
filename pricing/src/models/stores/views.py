from flask import Blueprint


store_blueprint = Blueprint(name='stores', import_name='__name__')


@store_blueprint.route('/store/<string:name>')
def store_page(name: str):
    pass


