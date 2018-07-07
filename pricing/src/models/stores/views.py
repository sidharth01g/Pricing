from flask import Blueprint, render_template, request, redirect, url_for
from pricing.src.models.stores.store import Store

store_blueprint = Blueprint(name='stores', import_name='__name__')


@store_blueprint.route('/', strict_slashes=False)
def index():
    stores = Store.get_all_stores()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>', strict_slashes=False)
def store_page(store_id: str):
    store = Store.find_one_by_id(_id=store_id)
    if not store:
        return redirect(location=url_for(endpoint='.index'))
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_store():
    if request.method == 'POST':
        return 'create post'
    return render_template('stores/create_store.html')
