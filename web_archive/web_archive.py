#######################
# @author: RaffaDNDM
# @date:   2022-09-24
#######################

import requests
import os
from termcolor import cprint
from urllib.parse import urlparse
import os
from alive_progress import alive_bar
import argparse

# HTTP Proxy to redirect traffic to Burp Suite
proxy = '127.0.0.1:8080'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['REQUESTS_CA_BUNDLE'] = "./certificate.pem" #PEM file generated from Burp Suite certificate

def web_archive_request(domain, output_folder):
    URL = f'https://web.archive.org/cdx/search/csx?url={domain}*&output=txt'

    #Read txt results and store request result in a TXT file with name "domain.txt"
    print(domain, end='\t')
    with requests.get(URL, stream=True) as r:
        if r.text:
            # OK (Some URLs identified for searched domain on Web Archive)
            with open(os.path.join(output_folder, f'{domain}.txt'), 'w') as f:
                #Write response results in "domain.txt" file
                f.write(r.text)
                cprint('File created!', 'green')
        else:
            #EMPTY (No URLs identified for searched domain on Web Archive)
            cprint('empty', 'red')

def input_parameters():
    """
    Parse command line parameters.

    Return
    ----------
    targets_file (str): Path of the targets file to be analysed.
    """
    
    #Define argument parser
    parser = argparse.ArgumentParser()
    #Create command line arguments
    parser.add_argument('--input', '-in', dest='targets_file', help='Path of the targets file to be analysed.')  
    parser.add_argument('--output', '-out', dest='output_folder', help='Path of the folder for output files.')
    #Parse command line arguments
    args = parser.parse_args()

    targets_file = args.targets_file
    #Ask user input filename if invalid as command line argument
    if (not targets_file) or (not os.path.exists(targets_file)):
        print('___Targets file___')
        targets_file = input()

    output_folder = "output"
    #Ask user input filename if invalid as command line argument
    if args.output_folder:
        output_folder = args.output_folder

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    return targets_file, output_folder

def csv_generator(output_folder):
    RESOURCES_SET=set()
    
    # For each file (one for each domain)
    for domain_results in os.listdir(output_folder):
        domain = domain_results.replace('.txt', '')
        
        #Read the content of the file
        with open(os.path.join(output_folder, domain_results), 'r') as f:
            #The third element of each line is the URL
            URLs = [x.split(" ")[2] for x in f.readlines()]

            #Store the URL in the final set (removing duplicates)
            for URL in URLs:
                RESOURCES_SET.add(URL)

    #For each URL in the set, verify reachability status by sending a GET request through Burp proxy
    with alive_bar(len(RESOURCES_SET)) as bar:
        for URL in sorted(RESOURCES_SET):
            x = urlparse(URL)
            path, extension = os.path.splitext(x.path)
            try:
                response = requests.get(URL, timeout=10)

            except requests.exceptions.ReadTimeout:
                pass

            bar()

def main():
    targets_file, output_folder = input_parameters()

    #Read input targets file
    with open(targets_file) as f:
        domains = [x.replace("\n", "").strip() for x in f.readlines()]

    #For each domain, request info about URLs on Web Archive
    for d in domains:
        web_archive_request(d, output_folder)

    # Final CSV results file generator from every CSV files
    csv_generator(output_folder)    

if __name__=='__main__':
    main()