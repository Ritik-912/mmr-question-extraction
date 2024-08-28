
# PDF Collection for Multimodal and Multilingual Reasoning Tasks


This repository is dedicated to collecting PDFs from the National Digital Library of India (https://ndl.iitkgp.ac.in/) for use in multimodal and multilingual reasoning tasks. The process involves multiple steps and scripts, running on both Windows and Linux machines, to ensure the accurate and comprehensive collection of PDF URLs and their subsequent downloads.



## Repository Overview


The repository contains the following scripts and their respective purposes:


- **link_scrapper.py**: Scrapes initial PDF viewer links and saves them.
- **download_link_collector.py**: Collects exact PDF URLs from the viewer pages.
- **download_url_extractor.py**: Extracts download URLs from pre-download links.
- **missing_url.py**: Identifies missed URLs during the scraping process.
- **downloader.py**: Downloads the PDFs using the collected URLs.


## Detailed Process


### 1. Scraping PDF Viewer Links


- **Script**: `link_scrapper.py`
- **Environment**: Windows 11
- **Description**: Utilizes Selenium with Firefox browser to open the browsing page on the NDLI website and scrolls to load all the PDF viewer links.
- **Output**: `scrapped_url.csv` containing 52 PDF viewer links.


### 2. Collecting Pre-Download URLs


- **Script**: `download_link_collector.py`
- **Environment**: Windows 11
- **Description**: Collects the initial pre-download URLs from the viewer pages.
- **Output**: `pre_download_url.csv` containing 25 pre-download links.


### 3. Extracting Exact Download URLs


- **Script**: `download_url_extractor.py`
- **Environment**: Windows 11
- **Description**: Extracts the exact download URLs from the pre-download links.
- **Output**: `download_url.csv` containing 25 download links.


### 4. Downloading PDFs


- **Script**: `downloader.py`
- **Environment**: Linux
- **Description**: Downloads the PDFs using the URLs in `download_url.csv`.
- **Output**: All 25 PDFs were successfully downloaded.


## Final Output


After completing the above steps, we successfully downloaded 25 PDFs.


## Dependencies


Please ensure that you have the necessary dependencies installed and configured before running the scripts by installing libraries in `windows_requirements.txt` and `linux_requirements.txt`.



## Flow Diagram


```plaintext


+------------+      +-------------------------+      +----------------------+
|            | ---> | link_scrapper.py        | ---> | scrapped_url.csv     |
|   Start    |      +-------------------------+      | (52 links)           |
|            |                                     +----------------------+
+------------+
                   +-------------------------+      +----------------------+
                   | download_link_collector | ---> | pre_download_url.csv |
                   | .py                     |      | (25 links)           |
                   +-------------------------+      +----------------------+
                   +-------------------------+      +----------------------+
                   | download_url_extractor  | ---> | download_url.csv     |
                   | .py                     |      | (25 links)           |
                   +-------------------------+      +----------------------+
                   +-------------------------+      +----------------------+
                   | downloader.py           | ---> | All 25 PDFs          |
                   +-------------------------+      | downloaded           |
                                                    +----------------------+
                   +-------------------------+      
                   | Final Output: 25 PDFs   | 
                   | Downloaded              | 
                   +-------------------------+   

                   +-------------------------+      
                   | Future Work: Extract    | 
                   | Questions from PDFs     | 
                   +-------------------------+ 


```



---
