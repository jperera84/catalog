""" Application Module """
import os
import random
import string
import json
from string import letters
from flask import Flask, render_template, request, redirect, jsonify, url_for,\
                  flash, session as login_session, make_response
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from database_setup import BASE, User, Item
from dao import get_all_categories, insert_user, get_user_by_email_provider,\
                get_lates_items, get_user_by_id, get_category_by_id, get_items_by_category,\
                insert_item, get_item_by_id, update_item, delete_item, get_all_items

APP = Flask(__name__)

# Connect to Database and create database session
ENGINE = create_engine('sqlite:///catalog.db')
BASE.metadata.bind = ENGINE

DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@APP.route('/')
@APP.route('/catalog')
def show_catalog():
    """ Homepage """
    categories = get_all_categories()
    items = get_lates_items()
    return render_template("catalog.html", categories=categories, items=items)

@APP.route('/login')
def show_login():
    """ Login Page """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", pagename="Authentication", STATE=state)

@APP.route('/catalog/<int:category_id>/')
def show_catalog_by_category(category_id):
    """ Show Catalog By Category """
    category = get_category_by_id(category_id)
    if category:
        items = get_items_by_category(category_id)
        return render_template("catalog_cat.html", category=category, items=items)
    else:
        response = make_response(json.dumps('Invalid Category parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

@APP.route('/catalog/<int:category_id>/crud/<int:item_id>')
def show_item_crud(category_id, item_id=None):
    """ Show Item CRUD """
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    else:
        categories = get_all_categories()
        item = get_item_by_id(item_id)
        return render_template("item_crud.html", pagename="Add New Item", method="new",\
                                category_id=category_id, categories=categories, item=item)

@APP.route('/catalog/item/cup', methods=['POST'])
def post_item():
    """ Create or Update Item """
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    else:
        item_id = request.form['item_id']
        if item_id:
            item_name = request.form['item_name']
            item_description = request.form['item_description']
            category_id = request.form['category_id']
            user_id = login_session['user_id']
            filename = None
            if 'item_picture' in request.files:
                file_var = request.files['item_picture']
                if file_var and allowed_file(file_var.filename):
                    filename = secure_filename(file_var.filename)
                    file_var.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            if item_name and item_description and category_id and user_id and item_id:
                item = get_item_by_id(item_id)
                if filename:
                    item.item_name = item_name
                    item.item_description = item_description
                    item.item_picture = filename
                    item.category_id = category_id
                else:
                    item.item_name = item_name
                    item.item_description = item_description
                    item.category_id = category_id
                update_item(item_id, item)
                if item_id:
                    return redirect(url_for('show_catalog_by_category', category_id=category_id))
            else:
                flash('Some of the fields are empty')
                return redirect(url_for('show_item_crud', category_id=category_id))
        else:
            item_name = request.form['item_name']
            item_description = request.form['item_description']
            category_id = request.form['category_id']
            user_id = login_session['user_id']
            filename = None
            if 'item_picture' in request.files:
                file_var = request.files['item_picture']
                if file_var and allowed_file(file_var.filename):
                    filename = secure_filename(file_var.filename)
                    file_var.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            if item_name and item_description and category_id and user_id:
                if filename:
                    item = Item(item_name=item_name, item_description=item_description,\
                                item_picture=filename,\
                                item_price=0.0, category_id=category_id, user_id=user_id)
                else:
                    item = Item(item_name=item_name, item_description=item_description,\
                                item_price=0.0, category_id=category_id, user_id=user_id)
                item_id = insert_item(item)
                if item_id:
                    return redirect(url_for('show_catalog_by_category', category_id=category_id))
            else:
                flash('Some of the fields are empty')
                return redirect(url_for('show_item_crud', category_id=category_id))

@APP.route('/catalog/item/del', methods=['POST'])
def del_item():
    """ Delete Item """
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    else:
        item_id = request.form['item_id']
        if item_id:
            item = get_item_by_id(item_id)
            delete_item(item_id)
            return redirect(url_for('show_catalog_by_category', category_id=item.category_id))
        else:
            return redirect(url_for('show_catalog'))

@APP.route('/catalog/JSON')
def catalog_json():
    """ Return JSON representation of the catalog """
    items = get_all_items()
    return jsonify(Items=[i.serialize for i in items])


def allowed_file(filename):
    """ Verify if the file extension is an image """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/gconnect', methods=['POST'])
def gconnect():
    """ Validate token """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http_var = httplib2.Http()
    result = json.loads(http_var.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    email = data['email']
    if email:
        user = get_user_by_email_provider(email, "Google")
        if user is None:
            user = User()
            user.user_name = data['name']
            user.user_email = email
            user.user_picture = data['picture']
            user.user_provider = "Google"
            user.user_id = insert_user(user)
            login_session['user_id'] = user.user_id
        else:
            login_session['user_id'] = user.user_id
    output = 'Successful'
    return output

@APP.route('/logout')
def logout():
    """ Logout """
    user_id = login_session['user_id']
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            if user.user_provider == "Google":
                access_token = login_session['access_token']
                if access_token is None:
                    response = make_response(
                        json.dumps('Current user not connected.'), 401)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
                http_var = httplib2.Http()
                result = http_var.request(url, 'GET')[0]
                if result['status'] == '200':
                    # Reset the user's sesson.
                    del login_session['access_token']
                    del login_session['gplus_id']
                    del login_session['username']
                    del login_session['email']
                    del login_session['picture']

                    response = make_response(json.dumps('Successfully disconnected.'), 200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                else:
                    # For whatever reason, the given token was invalid.
                    response = make_response(
                        json.dumps('Failed to revoke token for given user.', 400))
                    response.headers['Content-Type'] = 'application/json'
                    return response





SECRET = 'fart'
def make_secure_val(length=20):
    """ Make a Secure secret key """
    return ''.join(random.choice(letters) for x in xrange(length))

def shutdown_server():
    """ Utility function to stop the development server """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    APP.secret_key = make_secure_val()
    APP.debug = True
    APP.config['TEMPLATES_AUTO_RELOAD'] = True
    APP.run(host='0.0.0.0', port=5001)
    #shutdown_server()
        