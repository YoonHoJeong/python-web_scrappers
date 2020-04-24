from flask import Flask, render_template, request, redirect
from scrapper import get_jobs

app = Flask("SuperScrapper")
# 어플의 이름

db = {}
# 간단한 저장소를 만들고, 해당 key를 검색

# root route("/")로 접속 요청을 하면 파이썬 함수를 실행하도록 설정.
@app.route("/")
def home():
  return render_template("potato.html")
#2 html을 넣을 수도 있다.
#2 하지만 return에 모든 html을 넣는 것 X -> templates 폴더 생성
#2 render_template는 알아서 html을 찾아줌.


@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html",       searchingBy=word,
  resultsNumber=len(jobs),
  jobs=jobs 
  )
#3 데이터를 웹사이트에 보내고, 요청하는 모든 것 : request.
#3 flask에서 request 정보를 확인할 수 있다 - request.args.get()
#3 template으로 어떻게 데이터를 넘길 수 있을까? - render_template()안에 인자로 넣으면 됨. -> rendering

# route 아래에 오는 함수의 이름과 route의 이름이 같을 필요는 없다.
#  @ : 데코레이터, 바로 아래에 있는 '함수'만을 찾음.
#2 <username> : placeholder
#2   placeholder를 사용하면 route 함수에서 인자로 해당 placeholder의 변수를 받아야 한다.
# @app.route("/<username>")
# def contact(username):
#   return username + "contact me"

app.run(host="0.0.0.0")
# repl.it 환경에 있으므로 , host = "0.0.0.0"
# local에서 작업한다면 작동하지 않음.

