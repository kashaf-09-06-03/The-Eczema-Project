from flask import Flask
from flask import render_template , request , redirect , url_for
from database import create_table , add_posts , get_posts

app = Flask(__name__)
create_table()

@app.route("/" , methods=["GET" , "POST"])
def main():
    if request.method =="POST":
        form_name= request.form.get("form_name")
        if form_name == "blog_form":
            title=request.form["title"]
            content=request.form["content"]
            add_posts(Content=content , Title=title)
            
            
        return redirect(url_for("main"))
    ps = get_posts()
    return render_template("index.html" , POSTS = ps)


if __name__ == "__main__":
    app.run(debug=True)