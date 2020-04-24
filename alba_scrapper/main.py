import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

# 1. requests
# 2. 슈퍼 브랜드 채용 정보
#   div id = MainSuperBrand
#     class = goodsLogo goodsMain
        # ul goodsBox
        #   li impact
        #     a href 특성 으로 이동


def get_all_brands():
  result = requests.get(alba_url)

  # print(result)

  soup = BeautifulSoup(result.text, "html.parser")

  brands = soup.find("div",{"id":"MainSuperBrand"}).find("ul", {"class": "goodsBox"}).find_all("li", {"class": "impact"})

  brands_info = []

  for brand in brands:
    title = brand.find("span", {"class" : "company"}).string
    link = brand.find("a")["href"]
    brand_info = {'title': title, 'link': link}
    brands_info.append(brand_info)

  return brands_info



def get_brand_hire(brand):

  # brand - 'title', 'link'

  result = requests.get(brand['link'])
  soup = BeautifulSoup(result.text, "html.parser")
  # table - tbody
  #   tr : 각 지역별 채용 정보
  #     td  class = local
  #     td  class = title
  #       span  class = company
  #     td  class = data
  #     td  class = pay
  #       span class = payIcon hour
  #       span class = number
  #     td  class = regDate

  jobs = soup.find("div", {'id':"NormalInfo"}).find("table").find("tbody").find_all("tr")
  
  brand_data = []

  for job in jobs:

    tmp = job.find_all("td")
    if len(tmp) < 3:
      continue
    
    local = job.find_all("td")[0].text
    title = job.find("span", {"class": "company"}).string
    work_hour = job.find("td", {"class": "data"}).string
    pay_icon = job.find("span", {"class": "payIcon"}).string
    pay_value = job.find("span", {"class": "number"}).string
    reg_date = job.find("td", {"class": "regDate"}).string

    job_data = {'local': local, 'title': title, 'work_hour': work_hour, 'pay_icon': pay_icon, 'pay_value': pay_value, 'reg_date':reg_date}

    brand_data.append(job_data)

  return brand_data

def save_to_file(brand_name, brand_data):
  file = open(f"{brand_name}.csv", mode='w')
  writer = csv.writer(file)
  writer.writerow(["place", "title","time","pay","date"])

  for each_data in brand_data:
    writer.writerow(list(each_data.values()))
  
  file.close()

  return None

brands = get_all_brands()

count = 0

for brand in brands:
  print(f"{brand['title']} is processing...")
  brand_data = get_brand_hire(brand)
  save_to_file(brand['title'], brand_data)
  count = count + 1
