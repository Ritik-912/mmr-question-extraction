from pandas import read_csv, concat, DataFrame
DataFrame(concat([read_csv("download_url.csv"), read_csv("remaining_download_url.csv")], ignore_index=True)).to_csv("total_download_url.csv", index=False)
