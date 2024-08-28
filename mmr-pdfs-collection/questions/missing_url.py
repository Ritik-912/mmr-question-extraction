from pandas import read_csv, DataFrame
from tqdm import tqdm
total_links = read_csv('scrapped_url.csv')['url'].tolist()
found_links = read_csv('download_url.csv')['viewer_url'].tolist()
found_links.extend(read_csv('error_download_links.csv')['viewer_url'].tolist())
missing_links = [i for i in tqdm(total_links) if i not in found_links]
print('Number of missing links = ', len(missing_links))
DataFrame(missing_links, columns=['viewer_url']).to_csv('missed_url.csv')
