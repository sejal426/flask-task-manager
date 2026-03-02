#imports
from flask import Flask,render_template,request,redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#app
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db=SQLAlchemy(app)

#dataclass = row of data
class Mytask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    completed=db.Column(db.Integer,default=0)
    created=db.Column(db.DateTime,default=datetime.now)

    def __repr__(self)->str:
        return f"Task {self.id}"
    
with app.app_context():
        db.create_all()


#routes to webpages
#for creating and reading
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form.get("content")
        new_task = Mytask(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print (f"error :{e}")
            return f"error:{e}"
        
    #see all current tasks
    tasks=Mytask.query.order_by(Mytask.created).all()
    return render_template("index.html", tasks=tasks)
    #Mytask represents the table in your database.
    # Mytask.query means Go to the Mytask table and prepare to fetch data
    # .order_by(Mytask.created) Sort the tasks by the created column.
    # Get ALL the rows after sorting.Without .all(), nothing is actually executed.
    # Send the tasks data to the HTML file called index.html
    
#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"error:{e}"
    
#update a task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task=Mytask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
        
            return f"error:{e}"
    else:
        return render_template("update.html",task=task)
        
    
    
    
    
    
    
    
    
    
    



#runner and debugger
if __name__ == "__main__":
    
    app.run(debug=True)

