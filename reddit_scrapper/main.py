from flask import Flask, render_template, request, redirect
from scrapper import aggregate_subreddits, is_valid_subreddit

app = Flask("RedditNews")

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

@app.route("/add")
def add():
  new_subreddit = request.args.get('new-subreddit')

  start_with_r = False

  if len(new_subreddit) > 3:
    if new_subreddit[:3] == "/r/":
      start_with_r = True

  is_valid = is_valid_subreddit(new_subreddit)

  print(is_valid)

  if not is_valid or start_with_r:
    return render_template("notFound.html", startWithR=start_with_r)
  
  subreddits.append(new_subreddit)

  return render_template("home.html", subreddits=subreddits)


@app.route("/")
def home():
  print(subreddits)
  return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
  selected = []
  for subreddit in subreddits:
    if subreddit in request.args:
      selected.append(subreddit)
  posts = aggregate_subreddits(selected)
  posts.sort(key=lambda post: post['votes'], reverse=True)
  return render_template("read.html", selected=selected, posts=posts)


app.run(host="0.0.0.0")