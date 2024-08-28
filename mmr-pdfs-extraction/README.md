# mmr-pdfs-extraction
This will show the extraction process of questions from the large number of pdfs obtained in mmr-data-collection.

zip -r pdfs.zip ./questions ./graphs ./textbook ./charts
9.4G    ./pdfs.zip
python3.11 -m venv mmr_Venv
source mmr_Venv/bin/activate
pip install --upgrade -U pdfplumber pandas langdetect tqdm > install_log.out
nohup python eng_extract.py > eng_extract_log.out &
du -sh . 1.5G
mkdir eng_csv eng_json
mv ./*.csv eng_csv/
mv ./*.json eng_json/
merged csv and json files
917 englisgh pdf data extracted 1888 files links collected in `nonEnglish_pdfs.csv`
