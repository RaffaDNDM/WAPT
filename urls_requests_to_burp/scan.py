#######################
# @author: RaffaDNDM
# @date:   2023-06-08
#######################

import requests
import os
import urllib3
from ftplib import FTP
import time
from alive_progress import alive_bar

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = "http://127.0.0.1:8080"
proxies = {"http": proxy, "https": proxy}

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['REQUESTS_CA_BUNDLE'] = "./certificate.pem" #PEM file generated from Burp Suite certificate

with open("http.txt", "r") as f:
    urls = [x.replace("\n", "") for x in f.readlines()]

    with alive_bar(len(urls)) as bar, open("results.csv", "w") as f:
        for x in urls:
            try:
                r = requests.get(x, proxies=proxies, verify=False, timeout=5, allow_redirects=True)
                f.write(f"{x},{r.status_code}\n")
                time.sleep(0.3)
            except requests.exceptions.ReadTimeout as e:
                pass

            try:
                r = requests.options(x, proxies=proxies, verify=False, timeout=5, allow_redirects=True)
                time.sleep(0.3)
            except requests.exceptions.ReadTimeout as e:
                pass

            try:
                r = requests.head(x, proxies=proxies, verify=False, timeout=5, allow_redirects=True)
                time.sleep(0.3)
            except requests.exceptions.ReadTimeout as e:
                pass

            bar()

with open("ftp.txt", "r") as f:
    urls = [x.replace("\n", "") for x in f.readlines()]
    
    for x in urls:      
        print(x)
        ftp = FTP(x)  # connect to host, default port

        ftp.login()
        ftp.retrlines('LIST')