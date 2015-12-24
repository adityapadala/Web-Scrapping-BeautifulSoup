import requests
from bs4 import BeautifulSoup
import pandas as pd

class Yelp_Restaurants:
    
    def __init__(self, url):
        self.url = url
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content,'html.parser')
    
    def inspect(self):
    # to see the soup in a readable way using prettify
        print (self.soup.prettify())
    #to find all the links("a"). it returns a list
        self.soup.find_all("a")
    #iterate in the list and make it readable
        for link in self.soup.find_all("a"):
            print (link)
    #iterate in the list and get only the hyperlinks
        for link in self.soup.find_all("a"):
            print(link.get("href"))
    #iterate in the list and get the text
        for link in self.soup.find_all("a"):
            print(link.text)
    #iterate in the list and get the text
        for link in self.soup.find_all("a"):
            print(link.text , link.get("href"))
    #iterate in the list and get the text
        for link in self.soup.find_all("a"):
            print("<a href = '%s'>'%s'</a>" %(link.get("href"),link.text))

    def scrape(self):
        g_data = self.soup.find_all("div", {"class" : "search-result natural-search-result"})
        print(g_data)
        name=[]
        No_of_reviews=[]
        price=[]
        Category = []
        address=[]
        locality=[]
        contact=[]
        feedback=[]
        for item in g_data:
            name.append(item.contents[1].find_all("a",{"class":"biz-name"})[0].text)
    #extracting the number of review of the restuarants
            try:
                No_of_reviews.append(item.contents[1].find_all("span",{"class":"review-count rating-qualifier"})[0].text.replace('reviews','').strip())
            except:
                pass
    #extracting the expensiveness of the restuarants
            try:
                price.append(item.contents[1].find_all("span",{"class":"business-attribute price-range"})[0].text)
            except:
                pass
    #extracting the category of the restuarants
            try:
                Category.append(item.contents[1].find_all("span",{"class":"category-str-list"})[0].text.strip())
            except:
                pass
    #extracting the address of the restuarants
            try:
                address.append(item.contents[1].find_all("address")[0].text.strip())
                locality.append(item.contents[1].find_all("span",{"class":"neighborhood-str-list"})[0].text.strip())
                contact.append(item.contents[1].find_all("span",{"class":"biz-phone"})[0].text.strip())
            except:
                pass
    #extracting the reviews of the restuarants
            try:
                feedback.append(item.contents[3].find_all("p",{"class":"snippet"})[0].text.strip())
            except:
                pass
        Yelp_data = pd.DataFrame({'Name' : name, 'No_of_reviews' : No_of_reviews, 'price' : price,'Category': Category, 'address': address,
                         'locality': locality, 'contact': contact, 'feedback' : feedback})
        Yelp_data = Yelp_data[['Name', 'No_of_reviews', 'price','Category', 'address','locality', 'contact', 'feedback']]
        Yelp_data.to_csv('Yelp_Data.csv')

url_obj = Yelp_Restaurants("http://www.yelp.com/search?find_desc=Restaurants&find_loc=Hartford%2C+CT&ns=1")
url_obj.inspect()
url_obj.scrape()