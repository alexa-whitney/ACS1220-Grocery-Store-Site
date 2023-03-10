import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, ItemCategory
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()

    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
    
        flash('Success! The new STORE was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()

    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category =form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
        )
        db.session.add(new_item)
        db.session.commit()

        flash('Success! The new ITEM was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)

    # STRETCH - Add delete capability
    if form.delete.data:
        print('***ON THE RIGHT TRACK***')
        return redirect(url_for('main.delete_store', store_id=store.id)) 
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()

        flash('Good News! The store was UPDATED successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)

    # STRETCH - Add delete capability
    if form.delete.data:
        return redirect(url_for('main.delete_item', item_id=item.id)) 

    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()

        flash('Good News! The item was UPDATED successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)

@main.route('/delete/<item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = GroceryItem.query.get(item_id)
    # Stretch - delete the item
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Successfully deleted {} item'.format(item))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')

@main.route('/delete/<store_id>', methods=['GET', 'POST'])
def delete_store(store_id):
    store = GroceryStore.query.get(store_id)
    # Stretch - delete the item
    try:
        db.session.delete(store)
        db.session.commit()
        flash('Successfully deleted {} store'.format(store))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')