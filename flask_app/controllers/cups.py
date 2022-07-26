from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.cup import Cup
from flask_app.models.post import Post

@app.route('/cups')
def all_cups():
    if 'id' not in session:
        return redirect('/logout')
    mycups = Cup.get_mycups(session['id'])
    session['cup_type'] = ''
    return render_template('cups.html', user = User.get_one(session['id']), cups = Cup.get_all_cups(session['id']))

@app.route('/cups/get')
def get_cups():
    if 'id' not in session:
        return redirect('/logout')
    session['cup_type'] = '/get'
    data = {
        'id': session['id'],
        'type': 'get'
    }
    return render_template('cups.html', user = User.get_one(session['id']), cups = Cup.get_cups_by_type(data))

@app.route('/cups/give')
def give_cups():
    if 'id' not in session:
        return redirect('/logout')
    session['cup_type'] = '/give'
    data = {
        'id': session['id'],
        'type': 'give'
    }
    return render_template('cups.html', user = User.get_one(session['id']), cups = Cup.get_cups_by_type(data))

@app.route('/cups/mycups')
def my_cups():
    if 'id' not in session:
        return redirect('/logout')
    session['cup_type'] = '/mycups'
    return render_template('mycups.html', user = User.get_one(session['id']), mycups = Cup.get_mycups(session['id']))

@app.route('/add_cup')
def new_cup():
    if 'id' not in session:
        return redirect('/logout')
    return render_template('add_cup.html', user = User.get_one(session['id']))

@app.route('/create_cup', methods=['post'])
def create_cup():
    if not Cup.validate_cup(request.form):
        return redirect('/add_cup')
    # request.form['date']
    Cup.create(request.form)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')

@app.route('/cups/<int:cup_id>')
def view_cup(cup_id):
    if 'id' not in session:
        return redirect('/logout')
    session['cup_type'] = f'/{cup_id}'
    return render_template('view_cup.html', cup = Cup.get_one(cup_id), user = User.get_one(session['id']), posts = Post.get_cup_posts(cup_id))

@app.route('/cups/<int:cup_id>/edit')
def edit_cup(cup_id):
    if 'id' not in session:
        return redirect('/logout')
    return render_template('edit_cup.html', cup = Cup.get_one(cup_id), user = User.get_one(session['id']))

@app.route('/update_cup', methods=['post'])
def update_cup():
    cup_id = request.form['id']
    if not Cup.validate_cup(request.form):
        return redirect(f'/cups/{cup_id}/edit')
    Cup.update(request.form, cup_id)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')

@app.route('/cups/<int:cup_id>/del')
def delete_cup(cup_id):
    if 'id' not in session:
        return redirect('/logout')
    Cup.delete(cup_id)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')

@app.route('/+cup/<int:cup_id>')
def add_mycup(cup_id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'cup_id': cup_id,
        'follower_id': session['id'] 
    }
    Cup.add_mycups(data)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')

@app.route('/-cup/<int:cup_id>')
def rem_mycup(cup_id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'cup_id': cup_id,
        'follower_id': session['id'] 
    }
    Cup.rem_mycups(data)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')
# eof