import mechanize
import math
import re
import time
import smtplib
import locale
from bs4 import BeautifulSoup

locale.setlocale( locale.LC_ALL, '' )

username = "username"
password = "password"
fromaddr = "your@email.com"
toaddrs  = "destination@email.com"

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]

##log in##
br.open("http://nation-wars.com")
br.select_form(nr=0)
br.form['username'] = raw_input("Enter Username: ")
br.form['password'] = raw_input("Enter Password: ")
br.submit()
print "Logged In"
while True:
    market = br.open('http://game.nation-wars.com/nation_publicmarket.php?')
    br.select_form(nr=0)

    market_data = market.read()
    market_soup = BeautifulSoup(market_data, 'html.parser')

    bank_list = market_soup.find_all("table", {"width" : "70%"})
    bank_table = bank_list[0]
    trs = bank_table.find_all('tr')

    for tr in trs:
        cells = tr.find_all('td')
        bankAmount = cells[0].get_text()
        bankAmount = int(bankAmount[bankAmount.find("$") + 1:bankAmount.find("in the Nations") - 1].replace(".",""))
        
    market_list = market_soup.find_all("tr")
    market_table = market_list[26:33]

    row = 1
    for trow in market_table:
        cells = trow.find_all('td')

        ## Which unit you want to buy ##
        if cells[0].get_text() == "Ships":
            unitType = cells[0].get_text()
            unitQuantity = int(cells[4].get_text().replace(".",""))
            unitQuantity = int("100")
            if unitQuantity > 0:
                unitPrice = int(cells[3].get_text().replace("$","").replace(".",""))
                moneyNeeded = unitQuantity * unitPrice
                if moneyNeeded < bankAmount:
                    br.form["market[" + str(row) + "]"] = str(unitQuantity)
                    br.submit()
                    moneyLeft = bankAmount - moneyNeeded
                    msg = ('Purchased ' + locale.format("%d", unitQuantity, grouping=True) + ' ' + unitType + ' at ' + locale.currency(unitPrice, grouping=True) + ' costing '  + locale.currency(int(moneyNeeded), grouping=True) + '. You have ' + locale.currency(int(moneyLeft), grouping=True) + ' left in your bank.')
                    server = smtplib.SMTP('smtp.gmail.com:587')
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(fromaddr, toaddrs, msg)
                    server.quit()
        row += 1
    time.sleep(120)