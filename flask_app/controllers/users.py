from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.cup import Cup
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route('/')
def default():
    if 'id' not in session:
        return render_template('login.html')
    return redirect('/cups')

@app.route('/register')
def registration():
    if 'id' not in session:
        return render_template('register.html')
    return redirect('/logout')

@app.route('/registration', methods=['post'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/registration')
    data = request.form.to_dict()
    data['pwd'] = bcrypt.generate_password_hash(request.form['pwd'])
    session['id'] = User.create(data)
    session['cup_type'] = 'all'
    return redirect('/cups')

@app.route('/login', methods=['post'])
def user_login():
    if not User.validate_login(request.form):
        return redirect('/')
    user_db = User.get_one_email({'email': request.form['email']})
    if not user_db:
        flash("Invalid email/password.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.pwd, request.form['pwd']):
        flash("Invalid email/password.", "login")
        return redirect('/')
    session['id'] = user_db.id
    session['cup_type'] = 'all'
    return redirect(f'/cups')

@app.route('/pantry')
def profile():
    if 'id' not in session:
        return redirect('/logout')
    id = session['id']
    return redirect(f'/pantry/{id}')

@app.route('/pantry/<int:id>')
def profiles(id):
    if 'id' not in session:
        return redirect('/logout')
    return render_template('view_user.html', user = User.get_one(id), cups = Cup.get_cups_by_userid(id))

@app.route('/edit_profile')
def edit_profile():
    if 'id' not in session:
        return redirect('/logout')
    return render_template('edit_profile.html', user = User.get_one(session['id']))

@app.route('/update_profile', methods=['post'])
def update_profile():
    if not User.validate_register(request.form):
        return redirect('/update_profile')
    data = request.form.to_dict()
    User.update_profile(data)
    return redirect('/pantry')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#eof