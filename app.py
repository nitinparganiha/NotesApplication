from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///friend.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Frieds(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    Fname=db.Column(db.String,nullable=False)



@app.route('/')
def hello_world():
    return render_template("nitin.html")

@app.route('/go')        
def Login():
     return render_template("Login.html")


if __name__=="__main__":
    app.run(debug=True,port=8080)

    from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True, cascade="all, delete-orphan")

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        notes = user.notes
        return render_template('index.html', notes=notes)
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect('/')
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/create_note', methods=['POST'])
def create_note():
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        user = User.query.filter_by(username=session['username']).first()
        note = Note(title=title, content=content, user=user)
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/update_note/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        user = User.query.filter_by(username=session['username']).first()
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()

        if note:
            note.title = title
            note.content = content
            db.session.commit()
            return jsonify({"message": "Note updated successfully"})
        else:
            return jsonify({"error": "Note not found"}), 404
    else:
        return redirect('/login')

@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()

        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({"message": "Note deleted successfully"})
        else:
            return jsonify({"error": "Note not found"}), 404
    else:
        return redirect('/login')


