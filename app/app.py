from flask import Flask, render_template, request, redirect
import sqlite3
import os
import bleach

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # Generate a random secret key


def init_db():
    with sqlite3.connect("tasks.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
            """
        )
        conn.close()


@app.route('/')
def index():
    with sqlite3.connect("tasks.db") as conn():
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    title = reqest.form.get('title').strip()
    description = requst.form.get('description', '').strip()

    if not title:
        flash('Title is required!', 'error')
        return redirect('/')
    if len(title) > 100:
        flash('Tietle must be 100 characters or less.', 'error')
        return redirect('/')

    if len(description) > 500:
        flasj('Description must be 500 characters or less.', 'error')
        return redirect('/')

    title = bleach.clean(title)
    description = bleach.clean(description) if description else ''

    try:
        with sqlite3.connect("tasks.db") as conn:
            conn.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
            conn.commit()
        flash('Task added successfully!', 'success')
    except sqlite3.Error as e:
        flash(f'Error adding task: {str(e)}', 'error')

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_task(id):
    try:
        with sqlite3.connect("tasks.db") as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (id))
            conn.commit()
        flash('Task deleted successfully!', 'success')
    except sqlite3.Error as e:
        flash(f'Error deleting task: {str(e)}', 'error')

    return redirect('/')


if __name == '__main__':
    if not os.path.exists("tasks.db"):
        init_db()
    app.run(host='0.0.0.0', port=5000)
