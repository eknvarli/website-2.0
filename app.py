# Blog App with Flask & Jinja


# Modules
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import sqlite3 as sql
import markdown


# Settings
app = Flask(__name__)
app.template_folder = 'jinja'
con = sql.connect('posts.db')
cur = con.cursor()

ADMIN_KEY = 'test123'


# Functions
def create_table():
    schem = 'CREATE TABLE IF NOT EXISTS posts(title TEXT, content TEXT)'
    cur.execute(schem)


# Router
@app.route('/')
def index():
    return render_template('pages/index.jinja')

@app.route('/panel')
def panel():
    return render_template('admin/panel.jinja')

@app.route('/panel/edit', methods=['POST'])
def edit_panel():
    if request.method == 'POST':
        adminkey = request.form.get('adminkey')
        if adminkey == ADMIN_KEY:
            return render_template('admin/edit.jinja')
        else:
            return redirect('/panel')
    else:
        return redirect('/')
    
@app.route('/add-post', methods=['POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        file = request.form.get('content')
        con = sql.connect('posts.db')
        cur = con.cursor()

        schem = f'INSERT INTO posts VALUES("{title}","{file}.md")'
        cur.execute(schem)
        if True:
            con.commit()
            con.close()
            return 'success!<br><a href="/">go home</a>'
    else:
        return redirect('/')
    
@app.route('/posts')
def posts():
    con = sql.connect('posts.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM posts')
    data = cur.fetchall()

    return render_template('pages/posts.jinja', data=data)

@app.route('/posts/<post>')
def view_post(post):
    content_file = open(f'./posts/{post}.md','r',encoding='utf-8')
    content_raw = content_file.read()
    content = markdown.markdown(content_raw)

    return render_template('pages/view-post.jinja', content=content)


# Run App
if __name__ == '__main__':
    create_table()
    app.run(debug=True)