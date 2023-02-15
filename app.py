from flask import Flask, render_template, request, session, redirect, send_file,Response
from flask_session import Session
import json
from dotenv import load_dotenv
import os
from dbconnect import get_bio, put_bio, get_projects, post_project, delete_project, post_skill,get_skills,delete_skill, post_work, get_work,delete_work,post_education,delete_education,get_education,update_job_role,update_email,add_cv,get_cv,add_avatar
import base64
import io
from PIL import Image
from mailer import send_mail

load_dotenv()

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    return render_template('index.html', BIO=get_bio(), PROJECTS=get_projects(), SKILLS=get_skills())

@app.route("/admin/login")
def login():
    if session.get("name"):
        return redirect("/admin")
    else:
        return render_template('admin.html')

@app.route("/admin",methods=["POST", "GET"])
def admin():
    if request.method == "GET":
        if session.get("name") is None:
            return redirect("/admin/login")
        if session.get("name"):
            return render_template("dashboard.html", BIO=get_bio(), PROJECTS=get_projects(), SKILLS=get_skills(), WORK=get_work(), EDUCATION=get_education())
    
    if request.method == "POST":
        user_name = request.form.get("username")
        env_name = os.environ.get("name")
        user_pass = request.form.get("password")
        env_pass = os.environ.get("password")

        print(user_name,env_name,user_pass,env_pass)

        if(env_name == user_name and env_pass == user_pass):
            session["name"] = user_name
            return render_template('dashboard.html', BIO=get_bio(), PROJECTS=get_projects(), SKILLS=get_skills(),WORK=get_work(), EDUCATION=get_education())

    return redirect("/admin/login")


@app.route('/resume', methods=['GET'])
def download_pdf():

    BIO=get_bio()
    b64 = BIO[3]['cv']['$binary']['base64']

    pdf_bytes = base64.b64decode(b64)

    with open("cv.pdf", "wb") as f:
        f.write(pdf_bytes)

    try:
        return send_file('cv.pdf', mimetype='application/pdf', as_attachment=True)
    except Exception as e:
        return str(e)
    return redirect("/")

@app.route("/resume.pdf")
def open_pdf():

    BIO=get_bio()
    b64 = BIO[3]['cv']['$binary']['base64']

    pdf_content = base64.b64decode(b64)
    return Response(pdf_content, content_type="application/pdf")


@app.route("/admin/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/update/bio", methods=["POST"])
def update_bio():
    bio = request.form.get("bio")
    id = request.form.get("id")

    put_bio(id,bio)
    return redirect("/admin")

@app.route("/add/project", methods=["POST"])
def add_project():
    name = request.form.get("name")
    description = request.form.get("description")
    technology_list = list(request.form.get("technology").split(" "))
    github = request.form.get("github")
    deployment = request.form.get("deployment")
    post_project(name,description,technology_list,github,deployment)
    return redirect("/admin")

@app.route("/delete/project", methods=["POST"])
def delete_project_url():
    _id = request.form.get("id")
    delete_project(_id)
    return redirect("/admin")

@app.route("/add/skill", methods=["POST"])
def add_skill_url():
    post_skill(request.form.get("skill"),request.form.get("category"),request.form.get("icon"))
    return redirect("/admin")


@app.route("/delete/skill", methods=["POST"])
def delete_skill_url():
    delete_skill(request.form.get("id"))
    return redirect("/admin")


@app.route("/add/work", methods=["POST"])
def add_work_url():
    post_work(request.form.get("location"),request.form.get("description"),request.form.get("time"))
    return redirect("/admin")

@app.route("/delete/work", methods=["POST"])
def delete_work_url():
    delete_work(request.form.get("id"))
    return redirect("/admin")

@app.route("/add/education", methods=["POST"])
def add_education_url():
    post_education(request.form.get("name"),request.form.get("program"),request.form.get("year"))
    return redirect("/admin")

@app.route("/delete/education", methods=["POST"])
def delete_education_url():
    delete_education(request.form.get("id"))
    return redirect("/admin")

@app.route("/update/jobrole",methods=["POST"])
def update_job_role_url():
    update_job_role(request.form.get("id"),request.form.get("job"))
    return redirect("/admin")

@app.route("/update/email",methods=["POST"])
def update_email_url():
    update_email(request.form.get("id"),request.form.get("email"))
    return redirect("/admin")


@app.route("/add/cv", methods=["POST"])
def add_cv_url():
    pdf_file = request.files.get("pdf_file")
    pdf_data = pdf_file.read()

    add_cv(request.form.get('id'),pdf_data)

    return redirect("/admin")

@app.route('/add/avatar', methods=['POST'])
def add_avatar_url():
    avatar = request.files.get("avatar")
    avatar_data = avatar.read()
    add_avatar(request.form.get('id'),avatar_data)

    BIO=get_bio()
    b64 = BIO[4]['avatar']['$binary']['base64']
    image_data = base64.b64decode(b64)
    stream = io.BytesIO(image_data)
    image = Image.open(stream)
    image.save("static/pic/avatar.png", "PNG")

    return redirect("/admin")

@app.route("/send/mail", methods=["POST"])
def send_mail_route():
    send_mail(request.form.get("email"),request.form.get("subject"),request.form.get("message"))
    return redirect("/#contact")

if __name__ == "__main__":
    app.run(host='0.0.0.0')