import requests
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
from scrapeListWebsites import ScrapeGoogleSearchClass

class ScrapeSitesListed:
    scrapeObject = ScrapeGoogleSearchClass
    url_list = scrapeObject.scrapeWebsiteList("list of porn sites")
    # URL of the website with the list of URLs
    print(url_list)
    website_url = url_list
    # Function to scrape a list of URLs from a given URL
    def scrape_urls(urlList):
        data = []
        countforwebsistes = 0
        if len(urlList) > 0:
            for url in urlList:
                countforwebsistes += 1
                print("bhai bhai" + str(countforwebsistes))
                try:
                    response = requests.get(url)
                except requests.exceptions.RequestException as e:
                    print("Failed to retrieve search results:", e)
                    continue
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Locate the list element by its HTML structure
                    list_items = soup.find_all("ol")
                    count = 0 
                    for item in list_items:
                        count += 1
                        print(count)
                        # Find the <a> tag within the <li> tag
                        list = item.find_all("li")
                        for listItem in list:
                            anchor = item.find("a")
                            if anchor and anchor.get("href"):
                                data.append(anchor["href"])
            res = []
            finalData = np.array(data)
            [res.append(x) for x in finalData if x not in res]
            return np.array(res)


    scraped_urls = scrape_urls(website_url)
    time.sleep(2)

    if len(scraped_urls) > 0:
        # Write the URLs to a text file
        with open("scraped_urls.txt", "w") as f:
            count = 0
            for url in scraped_urls:
                count += 1
                f.write(str(count) + ". " + url + "\n")
        print("URLs scraped and saved to 'scraped_urls.txt'")
    else:
        print("Failed to scrape the URLs.")
