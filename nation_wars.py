import mechanize
import math
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

class State(object):
 
    def __init__(self, statenation, attacks, space, networth, land, estgrab):
        self.statenation = statenation
        self.attacks = attacks
        self.space = space
        self.networth = networth
        self.land = land
        self.estgrab = estgrab

	
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]

##log in##
br.open("http://nation-wars.com")
br.select_form(nr=0)
br.form['username'] = raw_input("Enter Username: ")
br.form['password'] = raw_input("Enter Password: ")
br.submit()
statenum = raw_input("Enter State #: ")
grabamount = int(raw_input("Enter Smallest Grab: "))
##global events##
events = br.open('http://game.nation-wars.com/events.php?action=search&search%5Btimefrom%5D=36&search%5Btimeto%5D=0&search%5Bstateids%5D=&search%5Btags%5D=&search%5Battacktype%5D=1&search%5Bdisplaylimit%5D=800')
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
    if len(cells) == 5:
        attack_type.append(cells[0].get_text())
        attackers.append(cells[1].get_text())
        attack_status = cells[3].get_text()
        attack_status = attack_status[0:6]
        if attack_status != "Defeat":
            defenders.append(cells[2].get_text())              
        
defender_dict = {i:defenders.count(i) for i in defenders}

##all states##
states = br.open('http://game.nation-wars.com/scores-all.php')
data = states.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find_all("table", {"width" : "100%"})
state_table = table[6]
states_list = []
trs = state_table.find_all('tr')
c = 0
nation = ""
for tr in trs:
    if c == 1:
        cells = tr.find_all('td')
        if len(cells) == 7:
            x = State("state", "attacks", "", "land", "networth", "estgrab")
            x.statenation = cells[2].get_text() + cells[3].get_text()
            tempnation = x.statenation[x.statenation.find("[") + 1:x.statenation.find("]")]
            x.land = cells[4].get_text()
            if statenum == x.statenation[x.statenation.find("#") + 1:x.statenation.find(")")]:
                stateland = float(x.land.replace(".",""))
                nation = tempnation
            x.networth = cells[5].get_text()
            if defender_dict.has_key(x.statenation) is False:
                x.attacks = 0
            else:
                for i in defenders:
                    if i == x.statenation:
                        x.attacks = defenders.count(i)
            for d in range(0, 35 - len(x.statenation)):
                x.space += " "
        if statenum != x.statenation[x.statenation.find("#") + 1:x.statenation.find(")")] and tempnation != nation:
            states_list.append(x)
    c = 1

up_states_list = []
for s in states_list:
    land = float(s.land.replace(".",""))
    attacks = float(s.attacks)
    if statenum != x.statenation[x.statenation.find("#") + 1:x.statenation.find(")")]:
        if s.attacks != 0:
            s.estgrab = (land/stateland)*(land*.13)*(math.pow(.67,attacks))
            states_list.count(s) + 1
        else:
            s.estgrab = (land/stateland)*(land*.13)
            states_list.count(s) + 1
    
for st in states_list:
    if states_list.count(st) == 1:
        up_states_list.append(st)


up_states_list.sort(reverse=True, key=lambda x: x.estgrab) 
print " "
print "      State                      Attacks   Land      Networth    Estimated Grab"
print " "
for s in up_states_list:
    if s.estgrab > grabamount:
        print s.statenation, s.space, s.attacks ,"  ", s.land.replace(".",",") , "   " + s.networth.replace(".",",") + "   " + str(s.estgrab)
        print " "

raw_input()