# Gobuster scanner
The program will execute gobuster on several targets, read from an input file.

## Installation
```bash
pip3 install -r requirements.txt
```

## Cheat sheet
```bash
python3 multi_gobuster_scanner.py -in input_file.txt -c ACME
```
This command will execute `gobuster` on targets read from `input_file.txt` and write results to a file with current date (e.g. `ACME_dir_enum_20220910.txt`).
- `-in <FILE_PATH>` is mandatory;
- `-c <CUSTOMER NAME>` is not mandatory (by default the name of the output file will be `CUSTOMER_dir_enum_20220910.txt`)

## Help command
```bash
python3 multi_gobuster_scanner.py --help
```