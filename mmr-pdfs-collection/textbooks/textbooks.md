
# PDF Collection for Multimodal and Multilingual Reasoning Tasks


This repository is dedicated to collecting PDFs from the National Digital Library of India (https://ndl.iitkgp.ac.in/) for use in multimodal and multilingual reasoning tasks. The process involves multiple steps and scripts, running on both Windows and Linux machines, to ensure the accurate and comprehensive collection of PDF URLs and their subsequent downloads.


## Repository Overview


The repository contains the following scripts and their respective purposes:


- **link_scrapper.py**: Scrapes initial PDF viewer links and saves them.
- **download_link_collector.py**: Collects exact PDF URLs from the viewer pages.
- **missing_url.py**: Identifies missed URLs during the scraping process.
- **downloader.py**: Downloads the PDFs using the collected URLs.


## Detailed Process


### 1. Scraping PDF Viewer Links


- **Script**: `link_scrapper.py`
- **Environment**: Windows 11
- **Description**: Utilizes Selenium with Firefox browser to open the browsing page on the NDLI website and scrolls to load all the PDF viewer links.
- **Output**: `scrapped_url.csv` containing the initial list of PDF viewer links.


### 2. Collecting Exact PDF URLs


- **Script**: `download_link_collector.py`
- **Environment**: Windows 11
- **Description**: Extracts the exact PDF URLs from the viewer pages.
- **Output**:
  - `download_url.csv`: Contains 963 PDF links.
  - `error_download_links.csv`: Contains 46 error links.


### 3. Identifying Missed URLs


- **Script**: `missing_url.py`
- **Environment**: Windows 11
- **Description**: Identifies URLs that were missed during the initial collection.
- **Output**: `missed_url.csv` containing the missed URLs.


### 4. Collecting Remaining Missed Links


- **Manual Step**: Added the missed link using MS Excel in `download_url.csv`
- **Environment**: Windows 11
- **Description**: Collects the remaining missed PDF URLs.
- **Output**: Updated `download_url.csv` to contain 964 links.


### 5. Downloading PDFs

- **Script**: `downloader.py`
- **Environment**: Linux
- **Description**: Downloads the PDFs using the URLs in `download_url.csv`.



## Final Output

After completing the above steps, we successfully downloaded 937 PDFs.


## Dependencies

Please ensure that you have the necessary dependencies installed and configured before running the scripts by installing libraries in `windows_requirements.txt` and `linux_requirements.txt`.


## Flow Diagram


```plaintext


+------------+      +-------------------------+      +----------------------+
|            | ---> | link_scrapper.py        | ---> | scrapped_url.csv     |
|   Start    |      +-------------------------+      +----------------------+
|            | 
+------------+
                   +-------------------------+      +----------------------+
                   | download_link_collector | ---> | download_url.csv     |
                   | .py                     |      | error_download_links |
                   +-------------------------+      +----------------------+

                   +-------------------------+      +----------------------+
                   | missing_url.py          | ---> | missed_url.csv       |
                   +-------------------------+      +----------------------+
                   +-------------------------+      +----------------------+
                   | downloader.py           | ---> | excepted_download    |
                   +-------------------------+      | .csv                 |
                                                    +----------------------+
                   +-------------------------+      
                   | Final Output: 937 PDFs  | 
                   | Downloaded              | 
                   +-------------------------+   

                   +-------------------------+      
                   | Future Work: Extract    | 
                   | Questions from PDFs     | 
                   +-------------------------+ 


```



---
