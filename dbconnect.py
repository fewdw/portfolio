from flask import Flask, request, jsonify, abort
import pymongo as pymongo
from pymongo import MongoClient
import json
import os
from bson import json_util
from bson.objectid import ObjectId
import certifi
ca = certifi.where()

#Connection string 
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
connection_string = f"mongodb+srv://fewdw:{MONGODB_PASSWORD}@portfolio.wffp2d3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=ca)

database = client.portfolio

bio = database.bio
education = database.education
projects = database.projects
skills = database.skills
work = database.work
 
def get_bio():
    all_info = bio.find()
    return json.loads(json_util.dumps(all_info))

def put_bio(id,newbio):
    filter = {"_id":ObjectId(id[10:34])}
    updated_bio = {
        "desc":newbio
    }
    bio.replace_one(filter,updated_bio)

def get_projects():
    all_info = projects.find()
    return json.loads(json_util.dumps(all_info))

def post_project(name,description,technology,github,deployment):
    project =  {
        "name":name,
        "description":description,
        "technology":technology,
        "github":github,
        "deployment":deployment
    }
    projects.insert_one(project)

def delete_project(_id):
    projects.delete_one({"_id":ObjectId(_id)})


def get_skills():
    all_skills = skills.find()
    return json.loads(json_util.dumps(all_skills))


def post_skill(skill,category,icon):
    skill = {
        "skill":skill,
        "category":category,
        "icon":icon
    }
    skills.insert_one(skill)

def delete_skill(_id):
    skills.delete_one({"_id":ObjectId(_id)})

def get_work():
    all_work = work.find()
    return json.loads(json_util.dumps(all_work))

def post_work(location,description,time):
    work_di = {
        "location":location,
        "description":description,
        "time":time
    }
    work.insert_one(work_di)

def delete_work(_id):
    skills.delete_one({"_id":ObjectId(_id)})

def get_education():
    all_edu = education.find()
    return json.loads(json_util.dumps(all_edu))

def post_education(name,program,year):
    edu = {
        "name":name,
        "program":program,
        "year":year
    }
    education.insert_one(edu)

def delete_education(_id):
    education.delete_one({"_id":ObjectId(_id)})

def update_job_role(_id,newbio):
    filter = {"_id":ObjectId(_id)}
    updated_bio = {
        "job":newbio
    }
    bio.replace_one(filter,updated_bio)

def update_email(_id,email):
    filter = {"_id":ObjectId(_id)}
    updated_email = {
        "email":email
    }
    bio.replace_one(filter,updated_email)

def add_cv(_id,pdf):
    filter = {"_id":ObjectId(_id)}
    updated_cv = {
        "cv":pdf
    }
    bio.replace_one(filter,updated_cv)

def get_cv():
    return bio.find_one({"type": "cv"})

def add_avatar(_id,avatar):
    filter = {"_id":ObjectId(_id)}
    updated_avatar={
        "avatar":avatar
    }
    bio.replace_one(filter, updated_avatar)
