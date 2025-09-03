from flask import Flask
from flask import render_template , request , redirect , url_for , session
from database import create_table , add_posts , get_posts , delet_posts ,search ,add_project,get_project,delete_project
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
create_table()
app.secret_key="A(K>2V)QBNP),@#81ado?<welb++Qq"

upload_floder="static/uploads"
allowed_extensions={"png","jpg","jpeg","gif"}
app.config["UPLOAD_FOLDER"]=upload_floder    
        
def allowed_file(name):
    return '.' in name and name.rsplit('.',1)[1].lower() in allowed_extensions       
          
@app.route("/" , methods=["GET" , "POST"])
def main():
    if request.method =="POST":
        form_name= request.form.get("form_name")
        if form_name == "blog_form":
            title=request.form["title"]
            content=request.form["content"]
            file=request.files.get("image")
            
            image_path=None
            if file and allowed_file(file.filename):
                safe_file=secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"] ,safe_file))
                image_path=f"uploads/{safe_file}"

            add_posts(Content=content , Title=title , image=image_path)
            return redirect(url_for("main"))
    search_query=request.args.get("search")
    if search_query:
        ps=search(search_query=search_query) 
    else:   
        ps = get_posts()
    pr= get_project()
    return render_template("index.html" , admin=session.get("is_admin") , POSTS = ps ,PROJECT=pr)


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

allowed_image_extensions={"png","jpg","jpeg","gif"}
allowed_audio_extensions={"mp3","mp4","wav","ma4"}
allowed_pdf_extensions={"pdf"}
app.config["project_folder"]="static/project_folder"  

# os.makedirs(app.config["project_folder"], exist_ok=True)
  
def allowedfile(name,allowed_set):
    return '.' in name and name.rsplit('.',1)[1].lower() in allowed_set 

@app.route("/addproject" ,methods=["GET" ,"POST"])
def add_projects():
    if request.method=="POST" and session["is_admin"]==True:
        title=request.form["title"]
        content=request.form["content"]
        image_path =None
        audio_path=None 
        pdf_path = None
        image = request.files.get("image")
        if image and allowedfile(image.filename , allowed_image_extensions):
            safe_image=secure_filename(image.filename)
            image.save(os.path.join(app.config["project_folder"],safe_image))
            image_path = f"project_folder/{safe_image}"
            
        audio = request.files.get("audio")
        if audio and allowedfile(audio.filename , allowed_audio_extensions):
            safe_audio=secure_filename(audio.filename)
            audio.save(os.path.join(app.config["project_folder"],safe_audio))
            audio_path = f"project_folder/{safe_audio}"   
            
        pdf = request.files.get("pdf")
        if pdf and allowedfile(pdf.filename , allowed_pdf_extensions):
            safe_pdf=secure_filename(pdf.filename)
            pdf.save(os.path.join(app.config["project_folder"],safe_pdf))
            pdf_path = f"project_folder/{safe_pdf}"               
        add_project(title=title , Content=content , image=image_path , pdf=pdf_path , audio=audio_path)
    return redirect(url_for("main"))

@app.route("/deleteProject/<int:post_id>" , methods=["GET","POST"])
def delete_projects(post_id):
    if session["is_admin"] == True:
        delete_project(post_id=post_id)
    return redirect(url_for("main"))  

if __name__ == "__main__":
    app.run(debug=True)