from flask import Blueprint, render_template, request, redirect, url_for
from pricing.src.models.stores.store import Store
import pricing.src.models.stores.errors as store_errors
import json

store_blueprint = Blueprint(name='stores', import_name='__name__')


@store_blueprint.route('/', strict_slashes=False)
def index():
    stores = Store.get_all_stores()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>', strict_slashes=False)
def store_page(store_id: str):
    try:
        store = Store.find_one_by_id(_id=store_id)
    except store_errors.StoreNotFoundError:
        return redirect(location=url_for(endpoint='.index'))
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_store():
    if request.method == 'POST':
        store_name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(name=store_name, url_prefix=url_prefix, tag_name=tag_name, query=query)
        store.insert_into_database()
        return redirect(location=url_for(endpoint='.index'))
    return render_template('stores/create_store.html')


@store_blueprint.route('/delete/<string:store_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_store():
    if request.method == 'POST':
        return 'Delete store'
    return 'Enter store ID'


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_store():
    if request.method == 'POST':
        return 'Edit post'
    return 'Enter store ID'
