# TESTSSL CSV parser
The program will parse TESTSSL scan csv results, contained in an input folder.

## Installation
```bash
pip3 install -r requirements.txt
```

## Cheat sheet
### Parse all CSV results from TESTSSL scan
```bash
python3 testssl_parser.py -csv /Path/To/CSV_Folder
```
where:
- `/Path/To/CSV_Folder` is the folder containing TESTSSL CSV results files.

**Another execution modality:**
```bash
python3 testssl_parser.py
```
Then provide path of the folder containing TESTSSL CSV results files.

## Help command
```bash
python3 testssl_parser.py --help
```