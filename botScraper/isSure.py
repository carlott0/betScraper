

from bs4 import BeautifulSoup
import pandas as pd
from sympy import symbols, Eq, solve
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime


import sys

def find_surebet(odds1, odds2):
    sum_odds = (1/odds1) + (1/odds2)
    if sum_odds<1:
        message = 'OK!'
    else:
        message = 'no'
    return message
   

def find_surebet_t(odds1, odds2, odds3):
    sum_odds = (1/odds1) + (1/odds2)+(1/odds3)
    if sum_odds<1:
        message = 'OK!'
    else:
        message = 'no'
    return message
   
#stake1*odds1 = stake2*odds2

def beat_bookies(odds1, odds2, total_stake):
    x, y = symbols('x y')
    eq1 = Eq(x + y - total_stake, 0) # total_stake = x + y
    eq2 = Eq((odds2*y) - odds1*x, 0) # odds1*x = odds2*y
    stakes = solve((eq1,eq2), (x, y))
    total_investment = stakes[x] + stakes[y]
    profit1 = odds1*stakes[x] - total_stake
    profit2 = odds2*stakes[y] - total_stake
    benefit1 = f'{profit1 / total_investment * 100:.2f}%'
    benefit2 = f'{profit2 / total_investment * 100:.2f}%'
    dict_gabmling = {'Stake1':stakes[x], 'Stake2':stakes[y], 'Profit1':profit1, 'Profit2':profit2,
                    'Benefit1': benefit1, 'Benefit2': benefit2}
    return dict_gabmling


#####




link="https://www.oddschecker.com/it/calcio/partite-del-giorno"
link2="https://www.oddschecker.com/it/calcio"
print("Scraping from "+link2)


hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(link2,headers=hdr)
response = urlopen(req)

html_soup = BeautifulSoup(response, 'html.parser')



t=html_soup.find_all('div', class_ = '_2tehgH')


q=html_soup.find_all('div', class_='_1NtPy1')



teamsCasa=[]
teamsFuori=[]
quota1=[]
quotaX=[]
quota2=[]
i=0
for s in t:
	if i==0:
		teamsCasa.append(s.text)
		i=1
	else:
		teamsFuori.append(s.text)
		i=0

i=0
for qq in q:
	if i==0:
		quota1.append(qq.text)
		i=1
	elif i==1:
		quotaX.append(qq.text)
		i=2
	elif i==2:
		quota2.append(qq.text)
		i=0



link="https://www.kickoff.co.uk/over-under-2-5-goals/"
print("Scraping from "+link)


hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(link,headers=hdr)
response = urlopen(req)

html_soup = BeautifulSoup(response, 'html.parser')



t=html_soup.find_all('div', class_ = 'ko-awp-cell-team-names')


q=html_soup.find_all('div', class_='ko-widget-odds-type ko-widget-odds-type-odds_decimal')


teams=[]

quotaU=[]
quotaO=[]


for s in t:
	teams.append(s.text)
	
i=0
for qq in q:
	if i==0:
		quotaO.append(qq.text)
		i=1
	elif i==1:
		quotaU.append(qq.text)
		i=0

# current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
#carico sul file i ris
ff='./scraped/'+str(dt_string)+'.txt'
matchSure=[]
quotaUSure=[]
quotaOSure=[]


with open(ff, 'w') as f:
	#pd.set_option('display.max_rows', None)
	#dict_gambling = {'casa': teamsCasa, 'fuori': teamsFuori, '1': quota1, 'X': quotaX, '2': quota2}
				#Presenting data in dataframe
	#			df_gambling = pd.DataFrame.from_dict(dict_gambling)
	#			print(df_gambling, file=f)
	count=0
	i=0
	while i<len(teamsCasa):
		if  quota1[i] != '--' and  quotaX[i] != '--' and  quota2[i]!='--':
			if find_surebet_t(float(quota1[i]),float( quotaX[i]), float( quota2[i]))=='OK!':
				 count+=1				
				 print( teamsCasa[i]+"-"+ teamsFuori[i]+"\t\t"+ quota1[i]+"\t"+ quotaX[i]+"\t"+ quota2[i]+"\n", file=f)
				
		i+=1
	if count==0:
		print("nessuna sureBet 1X2", file=f)
	
	count2=0
	i=0
	while i<len(teams):
		if  quotaU[i] != '--' and  quotaO[i] != '--':
			if find_surebet(float(quotaO[i]),float( quotaU[i]))=='OK!':
				 count2+=1
				 print( teams[i]+"\t\t"+ quotaO[i]+"\t"+ quotaU[i]+"\n", file=f)
				 matchSure.append(teams[i])
				 quotaUSure.append(float(quotaU[i]))
				 quotaOSure.append(float(quotaO[i]))
		i+=1
			
	print("Trovate "+str(len(teamsCasa))+" quote 1X2, "+ str(len(teams))+" quote U 2.5 O 2.5, scritte su "+ff+" "+str(count)+" surebets 1x2, "+str(count2)+" surebets U 2.5 O 2.5" ) 
	if count2==0:
		print("nessuna sureBet U 2.5 e O 2.5", file=f)
	else:

		soldi=input("Quanto si desidera giocare per Over 2.5 e Under 2.5? ")
		i=0
		while i<count2:
			print(matchSure[i]+"\t"+ quotaOSure[i]+"\t"+ quotaUSure[i]+"\t"+beat_bookies(quotaOSure[i], quotaUSure[i], soldi))
			i+=1
			





##############

