import requests
from bs4 import BeautifulSoup
import pandas as pd
import geocoder
import matplotlib.pyplot as plt
import numpy as np

class ATP_Calendar:
    
    def __init__(self,url):
        self.url = url
        r=requests.get(self.url)
        self.soup = BeautifulSoup(r.content,'html.parser')
    
    def inspect(self):
        print (self.soup.prettify())
        for item in self.soup.find_all("a"):
            print (item.text , item.get("href"))
            print("<a href = '%s'>'%s'</a>" %(item.get("href"),item.text))
    
    def scrape(self):
        g_data = self.soup.find_all("tr", {"class" : "tourney-result"})
        #name, address, dates
        Tourn_name = []
        Tourn_Location = []
        Tourn_dates=[]
        singles = []
        doubles = []
        court=[]
        count1 = 0
        for item in g_data:
            try:
                Tourn_name.append(item.contents[3].find_all("a",{"class":"tourney-title"})[0].text)
                Tourn_Location.append(item.contents[3].find_all("span",{"class":"tourney-location"})[0].text.strip())
                Tourn_dates.append(item.contents[3].find_all("span",{"class":"tourney-dates"})[0].text.strip())
                #round of singles, round of doubles
                #if count1 != 48:
                    #singles round
                singles.append(item.contents[5].find_all("div",{"class":"item-details"})[0].contents[1].text.strip())
                    #doubles round
                doubles.append(item.contents[5].find_all("div",{"class":"item-details"})[0].contents[3].text.strip())
                    #court
                a = str(item.contents[5]).split('<div class="item-details">')[2][2:5]
                if a == 'Out':
                    court.append("Outdoor")
                else:
                    court.append("Indoor")
                count1 += 1
            except:
                pass

        #surface
        count3 = 0
        surface = []
        for i in range(2,len(self.soup.find_all("span", {"class" : "item-value"}))-1,4):
            if count3 != 48:
                surface.append(self.soup.find_all("span", {"class" : "item-value"})[i].contents[0].strip())
            count3 += 1
        #for tournament finances
        count4 = 0
        Tourn_price = []
        f_data = self.soup.find_all("td", {"class" : "tourney-details fin-commit"})
        for item in f_data:
            if count4 != 48:
                Tourn_price.append(item.contents[1].find_all("span",{"class":"item-value"})[0].text.strip())
            count4 += 1
        print(len(Tourn_name))
        print(len(Tourn_Location))
        print(len(Tourn_dates))
        print(len(singles))
        print(len(doubles))
        print(len(court))
        print(len(surface))
        Atp_Calendar = pd.DataFrame()
        Atp_Calendar = pd.DataFrame({'Tourn_Title' : Tourn_name, 'Location' : Tourn_Location, 'Dates' : Tourn_dates,'Rounds_Single': singles, 'Rounds_Doubles': doubles, 'Court': court, 'Surface': surface})
        Atp_Calendar = Atp_Calendar[['Tourn_Title', 'Location', 'Dates','Rounds_Single', 'Rounds_Doubles','Court', 'Surface']]
        Atp_Calendar.to_csv('Atp_Calendar.csv')
        return Atp_Calendar
        
    def process(self,Atp_Calendar):
        st = []
        en = []
        for i in range(len(Atp_Calendar.Dates)):
            st.append(Atp_Calendar.Dates[i].split(' - ')[0])
            en.append(Atp_Calendar.Dates[i].split(' - ')[1])
        Atp_Calendar['StartDate'] = st
        Atp_Calendar['EndDate'] = en
        Atp_Calendar.StartDate = pd.to_datetime(Atp_Calendar.StartDate)
        Atp_Calendar.EndDate = pd.to_datetime(Atp_Calendar.EndDate)
        Atp_Calendar[['Rounds_Single','Rounds_Doubles']] = Atp_Calendar[['Rounds_Single','Rounds_Doubles']].astype(int)
        lat = []
        lon = []
        for i in range(len(Atp_Calendar.Location)):
            lat.append(geocoder.google(Atp_Calendar['Location'][i]).latlng[0])
            lon.append(geocoder.google(Atp_Calendar['Location'][i]).latlng[1])
        Atp_Calendar['Latitude'] = lat
        Atp_Calendar['Longitude'] = lon
        return Atp_Calendar
    
    def visualise(self,df):
        df['No_of_days'] = df['EndDate'] - df['StartDate']
        df['No_of_days'] = df['No_of_days']/np.timedelta64(1,'D')
        df['No_of_days'] = df['No_of_days'].astype(int)
        
        #to check when are grandslams being played.
        plt.figure(figsize=(15,8))
        plt.bar(df.StartDate,df.Rounds_Single)
        plt.suptitle('Singles_Rounds vs Time', fontsize = 16)
        plt.xlabel('Dates', fontsize = 12)
        plt.ylabel('Number of Rounds', fontsize = 12)
        
        #to check how many days tourns are played
        plt.figure(figsize=(15,8))
        x=[]
        x= np.arange(66)
        plt.plot(x,df['No_of_days'])
        plt.xticks(x + 0.5, df['Tourn_Title'], rotation=90)
        plt.suptitle('Singles_Rounds vs Time', fontsize = 16)
        plt.xlabel('Tournaments', fontsize = 12)
        plt.ylabel('Number of Rounds', fontsize = 12)
        
        #to see the percentage of surfaces played over years
        plt.figure(figsize=(15,8))
        labels = ['Hard','Clay','Grass']
        size = [df['Surface'].value_counts()['Hard'] , df['Surface'].value_counts()['Clay'] , df['Surface'].value_counts()['Grass']]
        colour = ['Blue','Orange','lightgreen']
        plt.pie(size, labels=labels, colors = colour,autopct='%2.2f%%')
        plt.axis('equal')
     

url_obj = ATP_Calendar("http://www.atpworldtour.com/en/tournaments")
#url_obj.inspect()
df = url_obj.scrape()
df = url_obj.process(df)
url_obj.visualise(df)	 
        