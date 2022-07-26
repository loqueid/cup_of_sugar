from flask_app import app
from flask import redirect, request, session
from flask_app.models.post import Post

@app.route('/create_post', methods=['post'])
def create_post():
    cup_id = request.form['cup_id']
    if not Post.validate_post(request.form):
        return redirect(f'/cups/{cup_id}')
    Post.create(request.form)
    return redirect(f'/cups/{cup_id}')

# @app.route('/edit/<int:post_id>')
# def edit_band(post_id):
#     if 'id' not in session:
#         return redirect('/logout')
#     return render_template('edit.html', user = User.get_one(session['id']), band = Band.get_one(id))

@app.route('/del_post/<int:post_id>')
def delete_band(post_id):
    if 'id' not in session:
        return redirect('/logout')
    Post.delete(post_id)
    cup_type = session['cup_type']
    return redirect(f'/cups{cup_type}')
# eof