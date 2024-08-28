import requests
from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame
import re
from tqdm import tqdm
import time

# Constants
RETRY_LIMIT = 5  # Number of retry attempts for each URL
DELAY_BETWEEN_RETRIES = 2  # Delay in seconds between retries

# Read URLs
urls = read_csv("missed_url.csv")["viewer_url"].tolist()
viewer_links = "http://ndl.iitkgp.ac.in/module-viewer/viewer.php?id="
df = []
error_links = []

# Function to make a request with retries
def make_request_with_retries(url, headers, retry_limit, delay):
    for attempt in range(retry_limit):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return None

# Processing URLs
for url in tqdm(urls):
    link = "/".join(url.split("/")[4:]).split('?')[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/532.36',
        'Referer': url
    }
    
    # Make request with retries
    response = make_request_with_retries(viewer_links + link + "&domain=se", headers, RETRY_LIMIT, DELAY_BETWEEN_RETRIES)
    
    if response:
        soup = BeautifulSoup(response.content, features="html.parser")
        scripts = soup.find_all("script", {'type': 'text/javascript'})
        try:
            for script in scripts:
                match = re.search(r'"url":"(.*?)"', script.string)
                if match:
                    df.append({"pdf_url": "http://ndl.iitkgp.ac.in" + match.group(1), "viewer_url": url})
                    break
            else:
                raise ValueError("No match found in scripts")
        except:
            try:
                tag_link = soup.find("a", {"class": "btn btn-success"})['href']
                df.append({"pdf_url": tag_link, 'viewer_url': url})
            except:
                try:
                    src = soup.find("iframe")['src']
                    df.append({"pdf_url": src, 'viewer_url': url})
                except:
                    error_links.append({"viewer_url": url})
    else:
        error_links.append(url)

# Print the number of found links
print("Number of pdf links = ", len(df))

# Save the found links to a CSV file
DataFrame(df).to_csv("remaining_download_url.csv", index=False)

# Save error links to a CSV file if any
if len(error_links) > 0:
    DataFrame(error_links).to_csv("error_download_links(1).csv", index=False)
