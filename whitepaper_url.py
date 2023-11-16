from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import SECRETS
import urllib
import requests
from urllib.parse import quote
import time 
import numpy as np
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class cryptoafresh():

    def __init__(self) -> None:
        self.driver = None
        self.driver_on = False
        pass

    def get_wiki_link_of_cg_from_golden_sel(self,coingecko_name):
        # Open the webpage
        url = 'https://golden.com/search/' +quote(coingecko_name )
        for _ in range(10):
            try:
                self.driver.get(url)
                # Get all the hyperlinks on the page
                all_links = self.driver.find_elements(By.TAG_NAME,'a')
                break
            except StaleElementReferenceException:
                continue

        # Loop through each hyperlink and print their href attribute
        #Scan for all hyperlinks
        hyperlinks = [link.get_attribute('href') for link in all_links]
        #If a hyper link contains the name then we can conclude that the coin name initially from coin gecko is in the Golden Database
        for link in hyperlinks:
            if link == None:
                continue
            contains_wiki = False
            if 'wiki/' not in link:
                continue
            contains = True

            for word in [elem.lower() for elem in coingecko_name.split()]:
                if word not in link.lower():
                    contains = False
                    break

            if contains == True:
                # wiki_url = 'https://golden.com'+link + '/structured_data'
                wiki_url = link + '/structured_data'
                return wiki_url
        return None

    def get_wiki_link_of_cg_from_golden(self,coingecko_name):
        url = 'https://golden.com/search/' +quote(coingecko_name )
        print(url)
        response = requests.get(url)
        if response.status_code != 200:
            print("Connection Unsuccessful")
            return(False)
        
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')
        all_links = soup.find_all('a')

        #Scan for all hyperlinks
        hyperlinks = [link.get('href') for link in all_links]
        #If a hyper link contains the name then we can conclude that the coin name initially from coin gecko is in the Golden Database
        for link in hyperlinks:
            contains = False
            if 'wiki/' not in link:
                continue
            contains = True

            for word in [elem.lower() for elem in coingecko_name.split()]:
                if word not in link.lower():
                    contains = False
                    break

            if contains == True:
                wiki_url = 'https://golden.com'+link + '/structured_data'
                return wiki_url
        return None

    def golden_whitepapers_urls_sel(self, cg_name):
        golden_wiki_structured_data_url = self.get_wiki_link_of_cg_from_golden_sel(cg_name)
        if golden_wiki_structured_data_url == None:
            return (["No wiki_link"],[])
        # Make a GET request to the webpage using Selenium
        for _ in range(5):
            try:
                self.driver.get(golden_wiki_structured_data_url)
                # Find the unnested div containing the word 'Whitepaper'
                div_with_whitepaper = self.driver.find_elements(By.XPATH,"//div[contains(text(), 'Whitepaper') and not(descendant::div)]")
                break
            except StaleElementReferenceException:
                continue
                
        # print("div_whit: ",div_with_whitepaper)
        if div_with_whitepaper == [] or div_with_whitepaper == None:
            # print('No links to whitepaper')
            whitepaper_links = []
        else:
            # Find the next div
            next_div = div_with_whitepaper[0].find_element(By.XPATH, "./following-sibling::div")

            # Find all 'a' tags within this div
            a_tags = next_div.find_elements(By.TAG_NAME,'a')

            # Get the links
            whitepaper_links = [a_tag.get_attribute('href') for a_tag in a_tags]

            # Print the links
            # print('whitepaper_links: \n', whitepaper_links)



        # Find the unnested div containing the word 'Official Website'
        div_with_off_website = self.driver.find_elements(By.XPATH,"//div[contains(text(), 'Official Website') and not(descendant::div)]")
        if div_with_off_website == None or div_with_off_website == []:
            # print('No official website tag')
            website_links = []
        else:
            # Find the next div
            next_div = div_with_off_website[0].find_element(By.XPATH,"./following-sibling::div")
            # print(next_div)
            # Find all 'a' tags within this div
            a_tags = next_div.find_elements(By.TAG_NAME,'a')

            # Get the links
            website_links = [a_tag.get_attribute('href') for a_tag in a_tags]

            # Print the links
            # print('website_links: \n', website_links)

        # Close the browser
        return (whitepaper_links, website_links)


    def golden_whitepapers_urls(self,golden_wiki_structured_data_url):
        # make a GET request to the webpage
        response = requests.get(golden_wiki_structured_data_url)
        if response.status_code != 200:
            print('Connection Unsuccessful in golden_whitepapers_urls')
            return None,None

        # parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the unnested div containing the word 'Whitepaper'
        div_with_whitepaper = soup.find(lambda tag: tag.name == "div" and "Whitepaper" in tag.text and not tag.find('div'))
        if div_with_whitepaper == None:
            print('No links to whitepaper')
            whitepaper_links = []
        else:
            # find the next div
            next_div = div_with_whitepaper.find_next('div')

            # find all 'a' tags within this div
            a_tags = next_div.find_all('a')

            # get the links
            whitepaper_links = [a_tag.get('href') for a_tag in a_tags]

            # print the links
            print('whiepaper_links: \n',whitepaper_links)

        # find the unnested div containing the word 'Official Website'
        div_with_off_website = soup.find(lambda tag: tag.name == "div" and "Official Website" in tag.text and not tag.find('div'))
        if div_with_off_website == None:
            print('No official website tag')
            website_links = []
        else:
            # find the next div
            next_div = div_with_off_website.find_next('div')

            # find all 'a' tags within this div
            a_tags = next_div.find_all('a')

            # get the links
            website_links = [a_tag.get('href') for a_tag in a_tags]

            # print the links
            print('website_links: \n', website_links)
        return(whitepaper_links,website_links)
    
    def initialise_webdriver(self):
        # Set up the Selenium WebDriver
        # self.driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(options=options)


    def close_webdriver(self):
        self.driver.close()
        self.driver = None
        print("Closed webdriver.")

    def coingecko_whitepapers_urls(self,coingecko_url,beg = False):
        self.driver.get(coingecko_url)
        if beg == True:
            time.sleep(5 + np.random.uniform(0,2))
        div_with_website = self.driver.find_element(By.XPATH,"//span[contains(text(), 'Website')]/ancestor::div[1]")
        whitepaper_links = []
        website_links = []
        html_text = div_with_website.get_attribute('innerHTML')
        if 'Website' in div_with_website.text:
            inner_div = div_with_website.find_element(By.TAG_NAME,'div')
            a_tags = inner_div.find_elements(By.TAG_NAME,'a')
            for tag in a_tags:
                if 'Whitepaper' in tag.text:
                    whitepaper_links.append(tag.get_attribute("href"))
                else:
                    website_links.append(tag.get_attribute("href"))
        return(whitepaper_links,website_links)
    


    def coingecko_whitepapers_urls_bs4(self, coingecko_url):
        if not hasattr(self, 'session'):
            self.session = requests.Session()

        response = self.session.get(coingecko_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        div_with_website = soup.find('div', text=lambda t: 'Website' in t)

        whitepaper_links = []
        website_links = []
        if div_with_website:
            a_tags = div_with_website.find_all('a')
            for tag in a_tags:
                if 'Whitepaper' in tag.text:
                    whitepaper_links.append(tag['href'])
                else:
                    website_links.append(tag['href'])
        else:
            print("Doesn't contain a link")

        print("Websites: ", website_links)
        print("Whitepapers: ", whitepaper_links)

        return whitepaper_links, website_links

    
    def google_pdf_search(self,name):
        url ='https://www.google.co.uk/search?q='+name+'+whitepaper+filetype%3Apdf'
        response = requests.get(url)

        hyperlink_pdf = []
        if response.status_code == 200:
            #Get the first search result that is a pdf and contains the name of the crypto in the hyperlink
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            all_links = soup.find_all('a')
            for link in all_links:
                if name in link.get("href") and 'search' not in link.get("href") and '.pdf' in link.get("href"):
                    hyperlink_pdf.append('https://www.google.co.uk' +link.get("href"))
                    break
            if hyperlink_pdf == None:
                return None
            return(hyperlink_pdf)
        else:
            print("Connection Unsuccessful")
            return(None)
        #     file_name = hyperlink_pdf[0].split('/')[-1]  # Extract the file name from the URL
        #     pdf_index = file_name.find(".pdf") + 4  # Find the index of ".pdf" and add 4 to include the ".pdf" itself
        #     file_name = file_name[:pdf_index]
        #     response = requests.get(hyperlink_pdf[0])

        #     # Save the PDF file
        #     # with open('googlesearchpdfs/'+file_name, 'wb') as file:
        #     #     file.write(response.content)
        #     #     print(f"Downloaded {file_name}")
        #     return(file_name)
        # else:
        #     print("Connection unsuccessful")
        #     return(None)
    def googlepdfsearch_sel(self,name):

        url ='https://www.google.co.uk/search?q='+quote(name)+'+whitepaper+filetype%3Apdf'
        self.driver.get(url)
        links = self.driver.find_elements(By.XPATH,'//a[@href]')

        for link in links:
            if name in link.get_attribute("href") and 'search' not in link.get_attribute("href") and '.pdf' in link.get_attribute("href"):
                return(link.get_attribute("href"))

    
    def word_is_name(self,name):
        name = name.title()
        APP_ID = SECRETS.X_Parse_Application_Id
        API_KEY = SECRETS.X_Parse_REST_API_Key
        where = urllib.parse.quote_plus("""
        {
            "Name": "%s"
        }
        """ % name.title())
        url = 'https://parseapi.back4app.com/classes/Listofnames_Complete_List_Names?count=1&limit=0&where=%s' % where
        headers = {
            'X-Parse-Application-Id': f'{APP_ID}', # This is your app's application id
            'X-Parse-REST-API-Key': f'{API_KEY}' # This is your app's REST API key
        }
        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
        json_data = json.dumps(data, indent=2)

        #Investigate the 'count' key in our json response object
        for key,value in data.items():
            if key == "count":
                if value>0:
                    print(name, "is a name")
                    return(True)
                else:
                    print(name, "is not a Name")
                    return(False)
            else:
                continue
    
    def getpdffromurl(self,pdfurl,filename):
        response = requests.get(pdfurl)
        if response.status_code != 200:
            print("Connection Unsuccesful")
            return
        # filename = pdfurl.split('/')[-1]  # Extract the filename from the URL
        with open('./PDFS/'+filename+".pdf", 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded: {filename}')


