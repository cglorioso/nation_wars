import mechanize
import math
import re
import time
from bs4 import BeautifulSoup
from collections import OrderedDict


br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]

##log in##
br.open("http://nation-wars.com")
br.select_form(nr=0)
br.form['username'] = "Derek"
br.form['password'] = "bball234"
br.submit()

while True:
    ##public market##
    market = br.open('http://game.nation-wars.com/publicmarketbuy.php')

    market_data = market.read()
    market_soup = BeautifulSoup(market_data, 'html.parser')
    market_list = market_soup.find_all("table", {"width" : "80%"})
    market_table = market_list[1]

    trs = market_table.find_all('tr')

    skipRow = 0
    unitType = ""
    unitQuantity = ""
    unitPrice = ""
    moneyNeeded = ""
    bankAmount = ""
    row = 0
    for tr in trs:
        cells = tr.find_all('td')
        if skipRow == 1:
            if len(cells) == 6:
                unitType = cells[0].get_text()
                unitQuantity = cells[1].get_text().replace(".","")
                unitPrice = cells[2].get_text().replace("$","").replace(".","")
                if unitType == "Jets" or unitType == "Ships":
                    moneyNeeded = int(unitQuantity) * int(unitPrice)
                
                    bank = br.open('http://game.nation-wars.com/bank.php')
                    bank_data = bank.read()
                    bank_soup = BeautifulSoup(bank_data, 'html.parser')
                    bank_list = bank_soup.find_all("table", {"width" : "50%"})
                    bank_table = bank_list[0]
                    trows = bank_table.find_all('tr')
                    bankRow = 0
                    for trow in trows:
                        cells = trow.find_all('td')
                        if bankRow == 1:
                            bankAmount = int(cells[1].get_text().replace("$","").replace(".",""))
                        bankRow += 1
                    if moneyNeeded < bankAmount:
                        br.select_form(nr=0)
                        br.form['withdrawalAmount'] = str(moneyNeeded)
                        br.submit()
                        print "Withdrew", moneyNeeded, "for", unitType

                        br.open('http://game.nation-wars.com/publicmarketbuy.php')
                        br.select_form(nr=row)
                        br.form['purchaseAmount'] = str(unitQuantity)
                        br.submit()
                        print "Purchased" , unitQuantity, unitType, "at", unitPrice, "costing", moneyNeeded

            row += 1  
        skipRow = 1
    print "1"
    time.sleep(120)

