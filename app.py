from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = "" 
DB_PORT = "3306"
DB_NAME = "project_db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        titles = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=titles, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = ToDo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo = allTodo)

# display task
@app.route('/display', methods=['GET','POST'])
def show_task():
    dply_task = ToDo.query.all()
    return render_template('display.html', dply_task = dply_task)

# delete task
@app.route('/delete/<int:sno>')
def delete_task(sno):
    del_todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect('/')

# update task
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update_task(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        upd_todo = ToDo.query.filter_by(sno=sno).first()
        upd_todo.title = title
        upd_todo.desc = desc
        db.session.add(upd_todo)
        db.session.commit()
        return redirect('/')
    

    upd_todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', upd_todo = upd_todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
