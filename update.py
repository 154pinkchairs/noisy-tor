import os
import re
import time
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path

def rmold(config_file):
    """Remove old user agents from the given config file."""
    with open(config_file, "r") as config:
        conf_old = config.read()
        if conf_old.find("user_agents") != -1:
            os.system("chmod +x update-helper.sh && ./update-helper.sh -c")
            print("Old user agents removed.")
        else:
            print("You seem to be running this script for the first time.\n")

def scrape_uas(urls):
    #Scrape the latest user agents from the given URLs.
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
            }
    responses = [requests.get(url, headers=headers, timeout=10) for url in urls]
    soups = [bs(response.text, "lxml") for response in responses]
    ua_spans = [[soup.find_all("span", {"class": "code"}) for soup in soups]]
    uas = [[ua.text.split(",") for ua in ua_spans[i] if getattr(ua, "text") is not None] for i in range(len(ua_spans))]
    return uas

def exportandclean(uas, output_file):
    #Export the given user agents to the given file and clean the file.
    tmp = Path(output_file)
    tmp.touch(exist_ok=True)
    with open(output_file, "r+") as temp:
        # Export user agents to file
        for ua_list in uas:
            for ua in ua_list:
                temp.write(f"{ua}\n")
        temp.seek(0)
        # Clean file by removing duplicate and invalid user agents
        ua_list = []
        for line in temp:
            if line.startswith("Mozilla") or re.search(r"\d$", line):
                line = f'"{line.strip()}"'
            if line.endswith("KHTML") and temp.readline().startswith("like Gecko"):
                line = f"{line.strip()} like Gecko"
            if line not in ua_list:
                ua_list.append(line)
        temp.seek(0)
        temp.truncate()
        for ua in ua_list:
            temp.write(f"{ua}\n")
    print("User agents exported to file.")
    return ua_list

def update_config(ua_list, config_file):
    """Update the given config file with the given user agent list."""
    with open(config_file, "r+") as config:
        conf = config.read()
        conf = conf.replace("user_agents", str(ua_list))
        config.seek(0)
        config.truncate()
        config.write(conf)
    print("Config file updated.")


if __name__ == "__main__":

    # URLs to scrape user agents from
    urls = [
            "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/",
            "https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/",
            "https://developers.whatismybrowser.com/useragents/explore/software_name/safari/",
            "https://developers.whatismybrowser.com/useragents/explore/software_name/edge/",
            "https://developers.whatismybrowser.com/useragents/explore/software_name/opera/"
            ]

    # Config file to update with the latest user agents
    config_file = "config.json"

    # File to export the latest user agents to before updating the config file with them
    output_file = "ua__list"

    rmold(config_file)

    uas = scrape_uas(urls)

    ua_list = exportandclean(uas, output_file)

    update_config(ua_list, config_file)
