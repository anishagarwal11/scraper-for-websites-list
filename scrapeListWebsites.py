import requests
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re

class ScrapeGoogleSearchClass:
    # Search query
    def scrapeWebsiteList(query):
        # URL of Google search results
        queryString = str(query)
        google_search_url = "https://www.google.com/search?q="+ queryString
        link_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)  # Regular expression to match URLs
        links = []
        # Adding headers to mimic a real browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        driver = webdriver.Chrome()
        # Send a GET request to Google
        try:
            driver.get(google_search_url)
            time.sleep(2)  # Give time for the page to load
        except Exception as e:
            print("Failed to open the Google search page:", e)

        # if response.status_code == 200:
        #     # soup = BeautifulSoup(response.content, "html.parser")
        #     # search_results = soup.find_all("div")
        for _ in range(10):  # Example: Loop through 5 pages
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                search_results = soup.find_all("div")
                # search_results = driver.find_elements_by_css_selector(".tF2Cxc")
                for result in search_results:
                    anchor = result.find("a")
                    if anchor and anchor.get("href"):
                        data = anchor["href"]
                        link_match = link_pattern.search(data)
                        if link_match:
                            link = link_match.group()
                # Exclude links from specific domains (e.g., google.com)
                            if "google.com" not in link:
                                links.append(link)
                next_button = driver.find_element_by_id("pnnext")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException as e:
                print("Failed to find search results:", e)
            except Exception as e:
                print("An error occurred:", e)
        driver.quit()
        res = []
        finalData = np.array(links)
        [res.append(x) for x in finalData if x not in res]
        if res:
            print("Links extracted and saved to 'search_links.txt'")
            with open("search_links.txt", "w") as f:
                count = 0
                for link in res:
                    count += 1
                    f.write(str(count) + ". " + link + "\n")
            return res
        else:
            print("No links found in the search results.")
            return []
