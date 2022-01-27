from operator import add, truediv
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

        print(date_stamp)
        print(item[0].replace(","," "))
        print(f"${item[1]['price']}")
        print(item[1]['link'])
        print("-----------")        

        writetocsv([date_stamp, item[1]['price'], item[1]['link'], item[0].replace(","," ")], abs_file_path)
    
    if email_confirmation == True:
        if item[1]['price'] < config.price_threshold:
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
        smtp.login(config.USER_NAME_send, config.USER_PASS_send)
        message_body = f"Subject:{subject}\n\n{body}"
        smtp.sendmail(config.USER_NAME_receive, config.email_tosend, message_body)
        smtp.quit()
    except:
        email_confirmation == False
        smtp.quit()

def get_html(url: str):
    response = requests.get(address, headers=config.header_values)
    return response.text

search_term = input("GPU Search Input: ")
#price_threshold = int(input("Price Threshold: "))
#email_tosend = input("Email for Alerts: ")
#time_wait_secs = int(input("Repeat Timer (secs): "))

email_confirmation = True

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
                except:
                    pass
            
        sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
        abs_file_path = os.path.join(config.csv_folder, search_term + ".csv") 
        date_stamp = datetime.datetime.now().date()
        time_stamp = datetime.datetime.now().time()

        output_data()

        try:
            smtp = smtplib.SMTP("smtp.gmail.com",587)
            smtp.login(config.USER_NAME_send, config.USER_PASS_send)
            print ("Invalid Credentials! Check config.py for credentials.")

            if config.time_wait_secs > 60:
                print(f"Restarting in {config.time_wait_secs/60} minute(s)..")
            else:
                print(f"Restarting in {config.time_wait_secs} seconds..")
            time.sleep(config.time_wait_secs)
                   
        except Exception:    
            if config.time_wait_secs > 60:
                print(f"Restarting in {'{:.2f}'.format(config.time_wait_secs/60)} minute(s)..")
            else:
                print(f"Restarting in {config.time_wait_secs} seconds..")
            time.sleep(config.time_wait_secs)
