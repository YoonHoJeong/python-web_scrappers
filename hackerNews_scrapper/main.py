import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

urls = {
  'new': new,
  'popular': popular
}

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

def get_items(order_by):
  items = None

  existing_items = db.get(order_by)
  if existing_items:
    items = existing_items
  else:
    print(f"downloading {order_by}s...")
    items = requests.get(urls.get(order_by)).json()['hits']
    db[order_by] = items
  
  return items

@app.route("/")
def root():
  order_by = request.args.get('order_by')

  print(order_by)
  if order_by:
    order_by = order_by.lower()
  else:
    order_by = 'popular'

  get_items(order_by)
  return render_template("index.html", order_by=order_by, items=db[order_by])

@app.route("/:<id>")
def detail(id):
  url = make_detail_url(id)
  print(url)
  item = requests.get(url).json()

  return render_template("detail.html", item=item, children=item.get('children'))

app.run(host="0.0.0.0")