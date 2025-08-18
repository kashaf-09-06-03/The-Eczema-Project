from flask import Flask
from flask import render_template , request , redirect , url_for , session
from database import create_table , add_posts , get_posts , delet_posts ,search

app = Flask(__name__)
create_table()
app.secret_key="A(K>2V)QBNP),@#81ado?<welb++Qq"
        
@app.route("/" , methods=["GET" , "POST"])
def main():
    if request.method =="POST":
        form_name= request.form.get("form_name")
        if form_name == "blog_form":
            title=request.form["title"]
            content=request.form["content"]
            add_posts(Content=content , Title=title)
            return redirect(url_for("main"))
    search_query=request.args.get("search")
    if search_query:
        ps=search(search_query=search_query) 
    else:   
        ps = get_posts()
    return render_template("index.html" , admin=session.get("is_admin") , POSTS = ps)


@app.route("/login" , methods=["GET","POST"])
def login():
    if request.method == "POST":
        pass_admin = request.form["password"]
        if pass_admin =="123":
            session["is_admin"]=True
            return redirect(url_for("main"))
        else:
            session["is_admin"]=False  
    return render_template("login.html") 

@app.route("/delete/<int:post_id>" , methods=["GET","POST"])
def delete(post_id):
    if session["is_admin"] == True:
        delet_posts(post_id=post_id)
    return redirect(url_for("main"))  


if __name__ == "__main__":
    app.run(debug=True)