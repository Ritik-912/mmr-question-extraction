import requests
from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame
import re
from tqdm import tqdm

urls = read_csv("scrapped_url.csv").values.tolist()
viewer_links = "http://ndl.iitkgp.ac.in/module-viewer/viewer.php?id="
df = []
error_links = []
for url in tqdm(urls):
    link = "/".join(url[0].split("/")[4:]).split('?')[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/532.36',
        'Referer':url[0]}
    response = requests.get(viewer_links+link+"&domain=se", headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")
    scripts = soup.find_all("script", {'type': 'text/javascript'})
    try:
        for script in scripts:
            match = re.search(r'"url":"(.*?)"', script.string)
            df.append({'pdf_url': "http://ndl.iitkgp.ac.in"+match.group(1), 'viewer_url': url[0]})
            break
    except:
        try:
            tag_link = soup.find("a", {"class": "btn btn-success"})['href']
            df.append({'pdf_url': tag_link, 'viewer_url': url[0]})
        except:
            try:
                src = soup.find("iframe")['src']
                df.append({'pdf_url': src, 'viewer_url': url[0]})
            except:
                error_links.append({'viewer_url': url[0]})
print("Number of pdf links = ", len(df))
DataFrame(df).to_csv("download_url.csv", index=False)
if len(error_links) > 0:
    DataFrame(error_links).to_csv("error_download_links.csv", index=False)
