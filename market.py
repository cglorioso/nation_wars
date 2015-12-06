import mechanize
import math
import re
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

##global events##
events = br.open('http://game.nation-wars.com/publicmarketbuy.php')
data = events.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find_all("table", {"width" : "95%"})
event_table = table[0]
trs = event_table.find_all('tr')
attack_type = []
attackers = []
defenders = []

for tr in trs[1:]:
    cells = tr.find_all('td')
    if len(cells) == 2:
        attack_type.append(cells[0].get_text())
        attackers.append(cells[1].get_text())
        attack_status = cells[3].get_text()
        attack_status = attack_status[0:6]
        if attack_status != "Defeat":
            defenders.append(cells[2].get_text())              
        

raw_input()