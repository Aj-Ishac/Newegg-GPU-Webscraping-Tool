from bs4 import BeautifulSoup
import requests
import re
import csv
import datetime
import os
import smtplib
import config

def output_data():

    subject = "Updates: Pricelookup.tool"

    for item in sorted_items:

        body =  f"Here's an update on the item you've been tracking and its price! \nThank you for using Pricelookup.tool\n\nSearch Term: {search_term} Price: ${item[1]['price']} \n{item[0]} \n{item[1]['link']}"

        print(item[0])
        print(f"${item[1]['price']}")
        print(item[1]['link'])
        print("-----------")        

        writetocsv([date_stamp, time_stamp, f"${item[1]['price']}", item[1]['link'], item[0]], abs_file_path)

        if item[1]['price'] < price_threshold:
            sendmail(subject, body)
            #print(f"comparison check: {item[1]['price']} < {price_threshold}")
            #print(item[1]['price'])


def writetocsv(values, search_term):
    csvfile = open(search_term, "a", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(values)
    csvfile.close   

def sendmail(subject, body):
    smtp = smtplib.SMTP("smtp.gmail.com",587)
    #smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config.USER_NAME, config.USER_PASS)

    message_body = f"Subject:{subject}\n\n{body}"
    smtp.sendmail(config.USER_NAME, config.USER_NAME, message_body)
    smtp.quit()

def get_html(url: str):
    response = requests.get(address, headers=config.header_values)
    return response.text

search_term = input("Input graphic card to search: ")
#price_threshold = input("Email price threshold: ")

#search_term = None
price_threshold = 1135

address = f"https://www.newegg.com/p/pl?SrchInDesc={search_term}&N=100007709%204131"
page = get_html(address)
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}
for page in range(1, pages + 1):

    address = f"https://www.newegg.com/p/pl?SrchInDesc={search_term}&N=100007709%204131&page={page}"
    page = get_html(address)
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        link = None
        if parent.name != "a":
            continue
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",","")), "link": link}
        except:
            pass
    
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
abs_file_path = os.path.join(config.csv_folder, search_term + ".csv") 
date_stamp = datetime.datetime.now().date()
time_stamp = datetime.datetime.now().time()

writetocsv(["Date","Time","Price", "Source", "Name"], abs_file_path)
output_data()