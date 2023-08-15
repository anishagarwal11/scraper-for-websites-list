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
        link_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
        if len(urlList) > 0:
            for url in urlList:
                try:
                    response = requests.get(url)
                    time.sleep(5)
                except requests.exceptions.RequestException as e:
                    print("Failed to retrieve search results:", e)
                    continue
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Locate the list element by its HTML structure
                    list_items = soup.find_all("a")
                    for listItem in list_items:
                        if listItem and listItem.get("href"):
                            linkData = listItem["href"]
                            link_match = link_pattern.search(linkData)
                            if link_match:
                                link = link_match.group()
                                data.append(link)
            res = []
            finalData = np.array(data)
            [res.append(x) for x in finalData if x not in res]
            return np.array(res)

    scraped_urls = scrape_urls(website_url)

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
