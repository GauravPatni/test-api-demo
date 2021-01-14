import time


from flask import Flask, render_template, send_from_directory

app= Flask(__name__)


@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"

