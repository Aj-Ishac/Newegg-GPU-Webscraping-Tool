from operator import add
from bs4 import BeautifulSoup
import requests
import re
import csv
import datetime
import os
import smtplib
import config
import time

def output_data():
    subject = "Pricelookup.tool: Price Updates"
    body =  "Here's an update on the item you've been tracking!\n\n"
    
    for item in sorted_items:

        body_extended = f"{item[0]} \n{item[1]['link']}\nPrice: ${item[1]['price']}\n\nThank you for using Pricelookup.tool"

        print(item[0])
        print(f"${item[1]['price']}")
        print(item[1]['link'])
        print("-----------")        

        writetocsv([date_stamp, time_stamp, f"${item[1]['price']}", item[1]['link'], item[0]], abs_file_path)

        if item[1]['price'] < price_threshold:
            sendmail(subject, body + body_extended)

def writetocsv(values, search_term):
      
    csvfile = open(search_term, "a", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(values)
    csvfile.close   

def sendmail(subject, body):
    smtp = smtplib.SMTP("smtp.gmail.com",587)
    smtp.ehlo()
    smtp.starttls()
    try:
        smtp.login(config.USER_NAME, config.USER_PASS)
        message_body = f"Subject:{subject}\n\n{body}"
        smtp.sendmail(config.USER_NAME, config.USER_NAME, message_body)
        smtp.quit()
    except:
        smtp.quit()

def get_html(url: str):
    response = requests.get(address, headers=config.header_values)
    return response.text

search_term = input("Input graphic card to search: ")
#price_threshold = input("Email price threshold: ")
price_threshold = 1135


if __name__ == '__main__':
    
    while True:

        try:
            os.remove(abs_file_path)
        except Exception:
            pass

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
                    #[("3080 FTW", {'price':2999, "link":"www"})]
                except:
                    pass
            
        sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
        abs_file_path = os.path.join(config.csv_folder, search_term + ".csv") 
        date_stamp = datetime.datetime.now().date()
        time_stamp = datetime.datetime.now().time()

        writetocsv(["Date","Time","Price", "Source", "Name"], abs_file_path)
        output_data()

        try:
            smtp = smtplib.SMTP("smtp.gmail.com",587)
            smtp.login(config.USER_NAME, config.USER_PASS)
        except:
            print ("Invalid Credentials! Cannot use Email Alerts.")

        time_wait_secs = 20
        print(f"Restarting in {time_wait_secs/60} minute(s)..")
        time.sleep(time_wait_secs)
