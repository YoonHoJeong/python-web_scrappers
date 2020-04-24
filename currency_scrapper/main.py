import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

datas = []

def extract_string(tr):
  # return array of strings extracted from html

  tr = tr.find_all("td")
  result = []
  # print(tr)
  for t in tr:
    result.append(t.string)
  
  if result[2] is None:
    return None

  return result


def get_data():
  # datas[1] : country name
  # datas[2] : code
  result = requests.get(url)

  soup = BeautifulSoup(result.text, "html.parser")

  table = soup.find("table", {"class":"table table-bordered downloads tablesorter"})
  trs = table.find_all("tr")
  
  # remove head element
  trs.pop(0)

  for tr in trs:
    tmp = extract_string(tr)
    if tmp is not None:
      datas.append(tmp)

  for i in range(len(datas)):
    print("# " + str(i) + " " + datas[i][0])

def input_num():
  num = -1

  while num == -1:
    try:
      num = int(input())
    except:
      print("That wasn't a number.")
      num = -1
  
  return num

def input_country_num():
  num = input_num()
  
  if num not in range(len(datas)):
    print("choose a number from the list.")
    return input_country_num()

  return num



def choose_data():
  print("Where are you from? choose a country by number.\n")
  print("#: ", end = '')
  my_country_num = input_country_num()
  my_country = datas[my_country_num]

  print(f"{my_country[0]}\n")

  print("Now choose another country.\n")
  print("#: ", end = '')
  another_country_num = input_country_num()
  another_country = datas[another_country_num]
  print(f"{another_country[0]}\n")

  print(f"How many {my_country[2]} do you want to convert to {another_country[2]}")
  amount = input_num()

  transfer_data = {'my_country': my_country, 'another_country': another_country, 'amount': amount}

  return transfer_data


get_data()

transfer_data = choose_data()

my = transfer_data['my_country']
another = transfer_data['another_country']
amount = transfer_data['amount']

transfer_url = f"https://transferwise.com/gb/currency-converter/{my[2].lower()}-to-{another[2].lower()}-rate?amount={amount}"

result = requests.get(transfer_url)

soup = BeautifulSoup(result.text, "html.parser")

transfered = soup.find("input", {"class":"js-TargetAmount"})

transfered_amount = format_currency(transfered['value'], another[2])
my_amount = format_currency(amount, my[2])

print(f"{my_amount} is {transfered_amount}")
