from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_un.db'

db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

@app.route('/')
def blog_list():
    bloglar = Blog.query.all()
    return render_template('index.html', bloglar=bloglar)

@app.route('/blog/<int:id>/')
def blog_detail(id):
    blog = Blog.query.get(id)
    return render_template('blog_detail.html', blog=blog)

@app.route('/blog/create', methods=['GET', 'POST'])
def blog_create():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        blog = Blog(title=title, text=text)
        db.session.add(blog)
        db.session.commit()

        return redirect('/')
    
    return render_template('new_blog.html')


@app.route('/blog/<int:id>/delete/')
def blog_delete(id):

    blog = Blog.query.get(id)

    db.session.delete(blog)
    db.session.commit()

    return redirect('/')


@app.route('/blog/<int:id>/update/', methods=['GET', 'POST'])
def blog_update(id):

    blog = Blog.query.get_or_404(id)

    if request.method == 'POST':

        blog.title = request.form.get('title')
        blog.text = request.form.get('text')

        db.session.commit()

        return redirect('/')

    return render_template('update_blog.html', blog=blog)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

