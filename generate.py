#!/usr/bin/env python


#############################################
# Author: Sirres Raphael
# Date: 01.05.2014
# Description: Generates a new Flask project
#############################################

import os
import argparse
from distutils.dir_util import mkpath

# Command-Line Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", action="store", dest="project", help="Creates new flask project")
parser.add_argument("-a", "--app", action="store", dest="app", help="Creates new flask app")

# Current command line path
CWD = os.getcwd()
# Path separator
SEP = os.sep
# App folder path
APP_BASE = ''.join([SEP, "app", SEP])



def folder(*path):
	""" Create folder(s) (does not override) Example: folder(./foo/bar) """
	#print "Folder: " + type(path)
	mkpath(join(path))


def file(path, content):
	content = content if content else ""
	if not os.path.isfile(path):
		with open(path, 'w+') as f:
			f.write(content)

def append(path, content):
	if os.path.isfile(path):
		with open(path, "a") as f:
			f.write(content)

def join(l):
	""" Utility function wrapping ''.join(list) """
	return ''.join(list(l))

def isFile(name):
	return name and name.lower().endswith(('.html', '.css', '.py', '.js', '.jpeg', '.png', '.txt'))

def isFolder(name):
	if name:
		return True
	else:
		return False

def traverse(tree, path=CWD):
	""" Takes a dictionary(tree) as argument and generates the folder/file structure """
	for k, v in tree.iteritems():
		p = ''.join([path, SEP, k])
		print "Path: " + p
		if isFile(k):
			file(p, v)
		elif isFolder(k):
			folder(p)
			traverse(v, p)
			

#########################
### Project GENERATOR ###
#########################

def init():
	init = """from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

#Later on you'll import the other blueprints the same way:
#from app.posts.views import mod as postsModule
#app.register_blueprint(postsModule)
"""
	return init

def config():
	CCONFIG = """class Config(object):
	DEBUG = False
	TESTING = False
	DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
   	DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
   	DEBUG = True
   	print "DEVEL"

class TestingConfig(Config):
   	TESTING = True
"""
	return CCONFIG

def runpy():
	c = "from app import app\napp.run(debug=True)"
	return c

def requirements():
	return ""

def project(name="FirstProject"):
	html = "<html><head>%s</head><body>%s</body></html>"
	error404 = html % ("<title>Error 404</title>", "Not Found")
	base = html % ("""<title>{% block title %}My Site{% endblock %}</title>""", 
					"""{% block content %}{% endblock %}""")
	index = """{% extends "base.html" %}
{% block content %}
	Hello
{% endblock %}"""
	PROJECT_STRUCT = {
		name: {
			"app":{
				"templates":{
					"404.html": error404,
					"base.html": base,
					"index.html": index
				},
				"static":{
					"img":{},
					"js":{},
					"css":{}
				},
				"__init__.py":init()
			},
			"run.py":runpy(),
			"config.py":config(),
			"requirements.txt": requirements()
		}
	}
	return PROJECT_STRUCT

######################
### APP GENERATOR ####
######################

def blueprint(name):
	path = CWD + APP_BASE + "__init__.py"
	print path
	temp = """
from app.%s.views import mod as %sModule
app.register_blueprint(%sModule)""" % (name, name, name)
	# check if module is already included
	if temp not in open(path).read():
		with open(path, "a") as f:
			f.write(temp)

def views(app):
	views = """from flask import Blueprint, render_template, request, redirect

mod = Blueprint('%s', __name__, url_prefix='/%s')

@mod.route('/')
def home():
	return render_template("index.html")""" % (app.lower(), app.lower())
	return views

def app(name="FirstApp"):
	APP_STRUCT = {
		"app": {
			name:{
				"__init__.py" : "",
				"models.py" : "", 
				"views.py" : views(name),
				"forms.py" : ""
			}
		}
	}

	return APP_STRUCT

##############
#### Main ####
##############
if __name__ == "__main__":
	# Test Project Generation
	
	args = parser.parse_args()
	if args.project:
		traverse(project(args.project))
	elif args.app:
		traverse(app(args.app))
		blueprint(args.app)





