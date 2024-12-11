from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('gamejam.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            game_title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# الحصول على اتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('gamejam.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Jam Submission</title>
    </head>
    <body>
        <h1>Submit Your Game for the Game Jam</h1>
        <form action="/submit" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br>
            <label for="game_title">Game Title:</label>
            <input type="text" id="game_title" name="game_title" required><br>
            <label for="description">Description:</label>
            <textarea id="description" name="description" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
        <a href="/submissions">View Submissions</a>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    game_title = request.form['game_title']
    description = request.form['description']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO submissions (name, email, game_title, description) VALUES (?, ?, ?, ?)',
                   (name, email, game_title, description))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/submissions')
def submissions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions')
    submissions = cursor.fetchall()
    conn.close()

    submission_list = '<ul>'
    for submission in submissions:
        submission_list += f'<li><strong>{submission["game_title"]}</strong> by {submission["name"]}<br>Email: {submission["email"]}<br>Description: {submission["description"]}</li>'
    submission_list += '</ul>'

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Jam Submissions</title>
    </head>
    <body>
        <h1>Game Jam Submissions</h1>
        {submission_list}
        <a href="/">Back to Submission Form</a>
    </body>
    </html>
    '''

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
