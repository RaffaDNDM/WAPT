import os
import requests
import csv
from termcolor import colored

def download(url: str, dest_folder: str, filename: str):
    dest_folder = dest_folder.lower().replace(' ', '_')
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

     # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    if not os.path.exists(file_path):
        r = requests.get(url, stream=True)
        if r.ok:
            print(colored("Saving to: ",'green'), os.path.abspath(file_path))
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
    
        else:  # HTTP status code 4XX/5XX
            print(colored(f'Download failed [{r.status_code}]: ', 'red'), os.path.abspath(file_path))
    else:
        print(colored("Already installed: ", 'yellow'), os.path.abspath(file_path))


    #File merged di tutte le wordlist (senza duplicati) in ciascuna categoria se #files>1
    #Horizon custom (altra cartella)


def main():
    with open('wordlists.csv', 'r') as f:
        for row in csv.DictReader(f):
            download(row['URL'], dest_folder=row['Category'], filename=row['Filename'])

if __name__=='__main__':
    main()