from flask import Blueprint, render_template, request, redirect, url_for
from pricing.src.models.stores.store import Store
import pricing.src.models.stores.errors as store_errors
import json
import ast

store_blueprint = Blueprint(name='stores', import_name='__name__')


@store_blueprint.route('/', strict_slashes=False)
def index() -> str:
    stores = Store.get_all_stores()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>', strict_slashes=False)
def store_page(store_id: str) -> str:
    try:
        store = Store.find_one_by_id(_id=store_id)
    except store_errors.StoreNotFoundError:
        return redirect(location=url_for(endpoint='.index'))
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_store() -> str:
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
def delete_store(store_id: str) -> str:
    if request.method == 'POST':
        return 'Delete store {}'.format(store_id)
    return 'Enter store ID'


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_store(store_id: str) -> str:
    try:
        store = Store.find_one_by_id(_id=store_id)
    except store_errors.StoreNotFoundError:
        return redirect(location=url_for(endpoint='.index'))

    if request.method == 'POST':
        store_name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = ast.literal_eval(request.form['query'])
        assert type(query) is dict

        store.name = store_name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query
        store.update_in_database(upsert=False)
        return redirect(location=url_for(endpoint='.index'))
    return render_template('stores/edit_store.html', store=store)
