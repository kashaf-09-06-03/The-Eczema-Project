from flask import Flask
from flask import render_template, request, redirect, url_for, session
from database import create_table, add_posts, get_posts, delet_posts, search, add_project, get_project, delete_project
import os
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
create_table()
app.secret_key = "A(K>2V)QBNP),@#81ado?<welb++Qq"

# Folder setup
app.config["UPLOAD_BLOGS"] = os.path.join(app.root_path, "static", "UPLOADBLOGS")
app.config["UPLOAD_PROJECTS"] = os.path.join(app.root_path, "static", "UPLOADPROJECTS")


# Auto-create folders if missing
os.makedirs(app.config["UPLOAD_BLOGS"], exist_ok=True)
os.makedirs(app.config["UPLOAD_PROJECTS"], exist_ok=True)

# Allowed extensions
allowed_image_extensions = {"png", "jpg", "jpeg", "gif"}
allowed_audio_extensions = {"mp3", "mp4", "wav", "m4a"}
allowed_pdf_extensions = {"pdf"}


def allowed_file(name, allowed_set):
    return "." in name and name.rsplit(".", 1)[1].lower() in allowed_set


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        form_name = request.form.get("form_name")

        # ---------- BLOG FORM ----------
        if form_name == "blog_form":
            title = request.form["title"]
            content = request.form["content"]
            file = request.files.get("image")

            image_path = None
            if file and allowed_file(file.filename, allowed_image_extensions):
                safe_file = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_BLOGS"], safe_file))
                image_path = f"UPLOADBLOGS/{safe_file}"  # stored relative path

            add_posts(Content=content, Title=title, image=image_path)
            return redirect(url_for("main"))

    # Search feature
    search_query = request.args.get("search")
    if search_query:
        ps = search(search_query=search_query)
    else:
        ps = get_posts()

    pr = get_project()
    return render_template("index.html", admin=session.get("is_admin"), POSTS=ps, PROJECT=pr)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass_admin = request.form["password"]
        if pass_admin == "123":
            session["is_admin"] = True
            return redirect(url_for("main"))
        else:
            session["is_admin"] = False
    return render_template("login.html")


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    if session.get("is_admin"):
        delet_posts(post_id=post_id)
    return redirect(url_for("main"))


@app.route("/addproject", methods=["GET", "POST"])
def add_projects():
    if request.method == "POST" and session.get("is_admin"):
        title = request.form["title"]
        content = request.form["content"]

        image_path = None
        audio_path = None
        pdf_path = None

        # Save image
        image = request.files.get("image")
        if image and allowed_file(image.filename, allowed_image_extensions):
            safe_image = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_PROJECTS"], safe_image))
            image_path = f"UPLOADPROJECTS/{safe_image}"

        # Save audio
        audio = request.files.get("audio")
        if audio and allowed_file(audio.filename, allowed_audio_extensions):
            safe_audio = secure_filename(audio.filename)
            audio.save(os.path.join(app.config["UPLOAD_PROJECTS"], safe_audio))
            audio_path = f"UPLOADPROJECTS/{safe_audio}"

        # Save PDF
        pdf = request.files.get("pdf")
        if pdf and allowed_file(pdf.filename, allowed_pdf_extensions):
            safe_pdf = secure_filename(pdf.filename)
            pdf.save(os.path.join(app.config["UPLOAD_PROJECTS"], safe_pdf))
            pdf_path = f"UPLOADPROJECTS/{safe_pdf}"

        add_project(title=title, Content=content, image=image_path, pdf=pdf_path, audio=audio_path)

    return redirect(url_for("main"))


@app.route("/deleteProject/<int:post_id>", methods=["GET", "POST"])
def delete_projects(post_id):
    if session.get("is_admin"):
        delete_project(post_id=post_id)
    return redirect(url_for("main"))

    

@app.route("/blog/<int:post_id>")
def blog_detail(post_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, title, content, image, time FROM posts WHERE id=?", (post_id,))
    post = cur.fetchone()
    con.close()
    
    if post:
        return render_template("blog_detail.html", post=post, admin=session.get("is_admin"))
    else:
        return redirect(url_for("main"))
    
    
@app.route("/project/<int:project_id>")
def project_detail(project_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, title, CONTENT, image_path, pdf_path, audio_path, time FROM projects WHERE id=?", (project_id,))
    project = cur.fetchone()
    con.close()
    
    if project:
        return render_template("project_detail.html", project=project, admin=session.get("is_admin"))
    else:
        return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
