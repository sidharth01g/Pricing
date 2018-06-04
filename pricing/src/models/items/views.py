rom flask import Blueprint

item_blueprint = Blueprint(name='item', import_name=__name__)


@item_blueprint.route('/item/<string:name>')
def item_page(name: str):
    pass


@item_blueprint.route('/load')
def load_item():
    pass