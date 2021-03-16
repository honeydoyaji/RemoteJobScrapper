from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_wework_jobs, get_ok_jobs, get_so_jobs
from exporter import save_to_file

app = Flask("myScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
      word = word.lower()
      existingJobs = db.get(word)  
      if existingJobs:              
          jobs = existingJobs
      else:
          jobs = get_ok_jobs(word) + get_so_jobs(word) + get_wework_jobs(word)
          db[word] = jobs
    else:
      return redirect("/")

    return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    # check if the word is on the url
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word) # bring jobs from fake db
    if not jobs:  # if ther is not job
      raise Exception()
    # if everything is there  
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

    
app.run(host='0.0.0.0', port=8080)