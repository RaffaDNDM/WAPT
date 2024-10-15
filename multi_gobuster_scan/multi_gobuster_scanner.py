#######################
# @author: RaffaDNDM
# @date:   2022-09-10
#######################

import subprocess
from datetime import datetime
from termcolor import cprint
import argparse
import os

def input_targets(input_file):
    #Read the list of targets (domains/IPs)
    with open(input_file, "r") as in_f:
        content=[x.replace("\n", "").strip() for x in in_f.readlines()]

    TARGETS = []

    #Create list of targets URL from domains/IPs
    for x in content:
        TARGETS.append("https://"+x.replace('\n', ''))
        TARGETS.append("http://"+x.replace('\n', ''))

    return TARGETS

def gobuster_run(TARGETS, customer):
    #Current time for output file name
    now = datetime.now()
    current_time = now.strftime("%Y%m%d")
    output_file=customer+"_dir_enum_"+now.strftime('%Y%m%d')+'.txt'
    print(output_file)
    input()

    #Open output file and execute gobuster for each target
    with open(output_file, "w") as f:
        for URL in TARGETS:
            cprint(f'{URL}', 'green')
            cprint('___________________________________________', 'green')

            cmd = ['gobuster',
            'dir',
            '-e',
            '-k',
            '-u',f'{URL}',
            '-t', '2',
            '-w','/usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-files.txt',
            '-x','.php,.asp,.aspx,.jsp,.js,.do,.action,.html,.json,.yml,.yaml,.xml,.cfg,.bak,.txt,.md,.sql,.zip,.tar.gz,.tgz']

            print(' '.join(cmd))
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
            count=0

            #Analyse output of gobuster command
            for line in p.stdout:
                line=line.decode('utf-8')
                line = line.replace(r'\r\n','')
                
                #Store only lines containing a resource found (containing 'Status' string)
                if "Status:" in line:
                    #Print the line on stdout
                    print(f'{line}')
                    #Store the line in output file
                    f.write(f"{line}")

                    count+=1

            p.wait()

            #Count number of resources found for the current target
            print(f'{count} resources found for ', end='') 
            cprint(f'{URL}', 'yellow', end='')
            print('.',end='\n\n')
            cprint('___________________________________________', 'green')

def input_parameters():
    """
    Parse command line parameters.

    Return
    ----------
    input_file (str): Name of file with targets IPs/domains (one for each line).

    customer (str): Customer name to be used in output file name.
    """    
    
    #Define argument parser
    parser = argparse.ArgumentParser()

    #Create command line arguments
    parser.add_argument('--input', '-in', dest='input_file', help='Input file with targets IPs/domains (one for each line).')
    #Create command line arguments
    parser.add_argument('--customer', '--client', '-c', dest='customer', help='Name of the customer without space')
    
    #Parse command line arguments
    args = parser.parse_args()

    #Ask user input filename if not provided as command line argument
    input_file=args.input_file
    while (not input_file) or input_file=='' or (not os.path.exists(input_file)):
        cprint('\n_Input file_', 'yellow')
        input_file = input()

    #Output file prefix
    customer='CUSTOMER'
    if args.customer and (args.customer != ''):
        customer=args.customer

    return input_file, customer

def main():
    #Parse CLI arguments
    input_file, customer = input_parameters()
    #Parse targets from input file
    TARGETS = input_targets(input_file)
    #Run gobuster for each target and store its results
    gobuster_run(TARGETS, customer)

if __name__=='__main__':
    main()