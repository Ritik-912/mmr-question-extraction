from pandas import DataFrame, read_csv
from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
extracted = []
not_extracted = []
for pdf_url, viewer_url in tqdm(read_csv("pre_download_url.csv").values.tolist()):
    try:
        response = get(pdf_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            link = soup.find("div", {"class": 'worksheet-pdf'}).find_all('a')
            for a in link:
                if a.get('href').endswith('.pdf'):
                    link = a.get('href')
                    link = '/'.join(pdf_url.split('/')[:3]) + link
                    break
            extracted.append([link, pdf_url, viewer_url])
        except:
            not_extracted.append([pdf_url, viewer_url])
    except:
        not_extracted.append([pdf_url, viewer_url])
if len(not_extracted) > 0:
    DataFrame(not_extracted, columns=["pdf_url", "viewer_url"]).to_csv("not_extracted_url.csv", index=False)
if len(extracted) > 0:
    print('pdf links extracted', len(extracted))
    DataFrame(extracted, columns=["link", "pdf_url", "viewer_url"]).to_csv("download_url.csv", index=False)