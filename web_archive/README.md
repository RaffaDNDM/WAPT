# Web Archive
The program will request information about URLs under target domains, using Web Archive. After obtains URLs from Web Archive, the program will perform GET requests to the URLs through **Burp Suite proxy**. The you save items from HTTP History of Burp to analyse requests and responses.

## Installation
```bash
pip3 install -r requirements.txt
```
## Certificate generation
### Download the certificat from Burp Suite url
- Open your web browser and go to http://burpsuite.
- Click on “CA Certificate” button on the top right corner and save the certificate locally.
![](resources/burocertificate.jpg)

### Convert the certificate to PEM encoded format
- The certificate downloaded is DER formated and needs to be PEM encoded. You need to run the following command:
    ```bash
    openssl x509 -inform der -in cacert.der -out certificate.pem
    ```

## Cheat sheet
### Parse all CSV results from TESTSSL scan
```bash
python3 web_archive.py -in targets.txt -out /Output/folder/path/
```
where:
- `targets.txt` is the path of the TXT file with the list of target domains.
- `/Output/folder/path/` is the path of the folder where a TXT file with Web Archive information will be stored for each domain in scope (By deafult `output` folder).

**Another execution modality:**
```bash
python3 web_archive.py
```
Then provide path of the TXT file with the list of target domains.

## Help command
```bash
python3 web_archive.py --help
```