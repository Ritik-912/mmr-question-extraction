
# PDF Collection for Multimodal and Multilingual Reasoning Tasks


This repository is dedicated to collecting PDFs from the National Digital Library of India (https://ndl.iitkgp.ac.in/) for use in multimodal and multilingual reasoning tasks. The process involves multiple steps and scripts, running on both Windows and Linux machines, to ensure the accurate and comprehensive collection of PDF URLs and their subsequent downloads.


## Repository Overview


The repository contains the following scripts and their respective purposes:


- **links.csv**: Manually save the 7 links from [NDLI](https://ndl.iitkgp.ac.in/se_browse/resourceType?resourceType%5B%5D=070000%2F070100&subjectClass%5B%5D=03000000&subjectClass%5B%5D=03000000%2F03010000) in an Excel sheet and save it as a CSV file.
- **downloader.py**: Downloads the PDFs using the collected URLs.


## Detailed Process


### 1. Downloading PDFs


- **Script**: `downloader.py`
- **Environment**: Linux
- **Description**: Downloads the PDFs using the URLs in `links.csv`.


## Dependencies

Please ensure that you have the necessary dependencies installed and configured before running the scripts by installing libraries in `requirements.txt`.



## Flow Diagram


```plaintext


+------------+      +-------------------------+      +----------------------+
|            | ---> | Manually Collect Links  | ---> | links.csv            |
|   Start    |      |                         |      | (7 links)            |
|            |      +-------------------------+      +----------------------+
+------------+
                   +-------------------------+      +----------------------+
                   | downloader.py           | ---> | All 7 PDFs           |
                   |                         |      | downloaded           |
                   +-------------------------+      +----------------------+
                   +-------------------------+
                   | Final Output: 7 PDFs    | 
                   | Downloaded              | 
                   +-------------------------+   

                   +-------------------------+      
                   | Future Work: Extract    | 
                   | Questions from PDFs     | 
                   +-------------------------+ 


```



---
