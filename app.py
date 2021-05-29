from flask import Flask,render_template,request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET','POST'])
def add_karo():
    if request.method == 'POST':
        print("yess")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template("index.html",allTodo=allTodo)
   
@app.route('/delete/<int:sno>')
def delete_karo(sno):
    
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update_karo(sno):
     if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
     todo=Todo.query.filter_by(sno=sno).first()
     return render_template("update.html",todo=todo)

@app.route('/home',methods=['GET'])
def home():
    return render_template("Home.html")

# way to api assmt
final_strg=[]

#one way
@app.route('/storestring' , methods=['POST'])
def store_strings():
  json_data = flask.request.json
  a_value = json_data["data"]
  final_strg.append(a_value)
  return a_value
  
#other way
@app.route('/postman_led/<name>',methods=['GET','POST'])
def post_wrk1(name):
    if request.method == 'POST':
        final_strg.append(name)
        return jsonify(name)


@app.route('/postman',methods=['GET','POST'])
def post_wrk():
    result=""
    for x in final_strg:
        result+=x
    return result
   #  final_strg+str(data)
#end assmt



if __name__=="__main__" :
    app.run(debug = True,port=8000)


