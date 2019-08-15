import requests
from bs4 import BeautifulSoup
import smtplib
import time

print("Hello, thank you for using my Amazon Price Tracker.")
print("Please answer the following questions!")
receiver = input("What is your email? ")
URL = input("Please enter the URL of item you would like to track: ")
goal = input("What is your desired price? (Do NOT include dollar sign): ")

cntr=0
def check_price():
    global cntr

    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    page = requests.get(URL, headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    title=title.strip()
    price = soup.find(id="priceblock_ourprice").get_text()

    converted_price = float(price[1:6])
    print("The product you have chosen to track is :",title[0:30],'...')
    print("The current price is:",converted_price)
    print("If the product price reaches your goal, you will be notified immediately. Otherwise, you will be updated once a week of the product's price.")

    if converted_price < float(goal):
        send_drop()
    if cntr==0:
        send_update()
    cntr+=1
    if cntr==7:
        cntr=0


def send_drop():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('____', '_____') #Enter sender email username, sender email password

    subject = 'Price Drop!'

    body = 'The amazon product you have been tracking dropped in price, go check it out! : https://www.amazon.com/Spikeball-Pro-Kit-Tournament-Upgraded/dp/B01M0XJYVO/ref=pd_lpo_sbs_200_t_1?_encoding=UTF8&psc=1&refRID=3BD7PC2CF68G6FTXAQYN'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'jdwallach1@gmail.com',  #Sender email
        receiver,
        msg
    )
    print("An email has been sent!")
    server.quit()


def send_update():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('jdwallach1@gmail.com', '1114095550127')

    subject = 'Weekly Update'

    body = 'The amazon product you have been tracking has not reached your price goal. Stay tuned!'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'jdwallach1@gmail.com', #sender email
        receiver,
        msg
    )
    print("An email has been sent!")
    server.quit()

while True:
    check_price()
    time.sleep(60*60*24)

