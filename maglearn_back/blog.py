from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort

from maglearn_back.auth import login_required
from maglearn_back.database import db
from maglearn_back.model import Post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user['id'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    try:
        post = Post.query.filter(Post.id == id).one()
    except NoResultFound:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id: int):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
