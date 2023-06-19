from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

# Comment model
class commentDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    status = db.Column(db.String(10), default='pending')

# Routes
@app.route('/',methods = ['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "POST":
        if username == "admin" and password == "admin":
            return redirect(url_for('admin'))
        elif username == "user" and password == "user":
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user',methods=["POST","GET"])
def user():
    comments = commentDatabase.query.all()
    return render_template("user.html", comments=comments)


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == "POST":
        text = request.form['text']

        comment = commentDatabase(text=text)
        db.session.add(comment)
        db.session.commit()
        return redirect('/user')

@app.route('/admin')
def admin():
    comments = commentDatabase.query.all()
    return render_template('admin.html', comments=comments)

@app.route('/approve_comment/<int:comment_id>')
def approve_comment(comment_id):
    comment = commentDatabase.query.get(comment_id)
    comment.status = 'approved'
    db.session.commit()
    return redirect('/admin')

@app.route('/reject_comment/<int:comment_id>')
def reject_comment(comment_id):
    comment = commentDatabase.query.get(comment_id)
    comment.status = 'rejected'
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
