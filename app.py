from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title

@app.route("/" , methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
    allTodo=Todo.query.all()
    return render_template('index.html',alltodo=allTodo)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        res = Todo.query.filter_by(sno=sno).first()
        res.title = title
        res.desc = desc
        db.session.commit()
        return redirect('/')

    res = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', res=res)


@app.route("/delete/<int:sno>")
def delete(sno):
    res = Todo.query.filter_by(sno=sno).first()
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
