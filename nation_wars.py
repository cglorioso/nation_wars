import mechanize, re
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]

##log in##
br.open("http://nation-wars.com")
br.select_form(nr=0)
br.form['username'] = raw_input("Enter username: ")
br.form['password'] = raw_input("Enter password: ")
# br.form['username'] = '-Chris-'
# br.form['password'] = 'owned'
br.submit()

##global events##
events = br.open('http://game.nation-wars.com/events.php?action=search&search%5Btimefrom%5D=36&search%5Btimeto%5D=0&search%5Bstateids%5D=&search%5Btags%5D=&search%5Battacktype%5D=1&search%5Bdisplaylimit%5D=800')
data = events.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find_all("table", {"width" : "95%"})
event_table = table[0]
trs = event_table.find_all('tr')
type =[]
attackers = []
defenders = []
for tr in trs[1:]:
    cells = tr.find_all('td')
    if len(cells) == 5:
        type.append(cells[0].get_text())
        attackers.append(cells[1].get_text())
        defenders.append(cells[2].get_text())       
        
defender_dict = {i:defenders.count(i) for i in defenders}

##all states##
states = br.open('http://game.nation-wars.com/scores-all.php')
data = states.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find_all("table", {"width" : "100%"})
state_table = table[6]
trs = state_table.find_all('tr')
for tr in trs:
    cells = tr.find_all('td')
    if len(cells) == 7:
        state_nation = cells[2].get_text() + cells[3].get_text()
        if defender_dict.has_key(state_nation) is False:
            defender_dict[state_nation] = 0
        


for state, count in defender_dict.items():
    print state, count