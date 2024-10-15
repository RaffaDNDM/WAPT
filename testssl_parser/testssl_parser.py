#######################
# @author: RaffaDNDM
# @date:   2022-09-24
#######################

import os
import argparse
from datetime import datetime
from termcolor import cprint
from alive_progress import alive_bar

# File MAP
# { (Column name in csv created by program) : (Column name in results CSV files from TESTSSL)}
SOCK_INFO = {
    "SSLv2" : "SSLv2",
    "SSLv3" : "SSLv3",
    "TLS 1" : "TLS1",
    "TLS 1.1" : "TLS1_1",
    "TLS 1.2" : "TLS1_2",
    "TLS 1.3" : "TLS1_3",
    "NPN/SPDY" : "NPN",
    "ALPN/HTTP2" : "ALPN"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
CIPHERS_TEST = {
    'NULL ciphers (no encryption)' : "cipherlist_NULL",
    'Anonymous NULL Ciphers (no authentication)' : "cipherlist_aNULL",
    'Export ciphers (w/o ADH+NULL)' : "cipherlist_EXPORT",
    'LOW: 64 Bit + DES; RC[2;4] (w/o export)' : "cipherlist_LOW",
    'Triple DES Ciphers / IDEA' : "cipherlist_3DES_IDEA",
    'Obsolete CBC ciphers (AES; ARIA etc.)' : "cipherlist_AVERAGE",
    'Strong encryption (AEAD ciphers)' : "cipherlist_STRONG"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
FORWARD_SECRECY = {
    'PFS is offered' : "PFS",
    'PFS Ciphers': "PFS_ciphers",
    'Elliptic curves offered' : "PFS_ECDHE_curves",
    'DH group offered' : "DH_groups"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
SERVER_PREFERENCES = {
    'Has server Cipher Order?' : "cipher_order",
    'Negotiated protocol' : "protocol_negotiated",
    'Negotiated cipher' : "cipher_negotiated",
    'Cipher Order' : "cipherorder_TLSv1_2"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
SERVER_DEFAULT = {
    "TLS extensions (standard)" : "TLS_extensions",
    "Session Ticket RFC 5077 hint" : "TLS_session_ticket",
    "SSL Session ID support" : "SSL_sessionID_support",
    "Session Resumption Ticket" : "sessionresumption_ticket",
    "Session Resumption ID" : "sessionresumption_ID",
    "TLS clock skew" : "TLS_timestamp",
    "Cert numbers": "cert_numbers",
    "Signature Algorithm" : "cert_signatureAlgorithm",
    "Server key size" : "cert_keySize",
    "Server key usage" : "cert_keyUsage",
    "Server extended key usage" : "cert_extKeyUsage",
    "Serial number" : "cert_serialNumber",
    "Serial number length" : "cert_serialNumberLen",
    "Fingerprint SHA1" : "cert_fingerprintSHA1",
    "Fingerprint SHA256" : "cert_fingerprintSHA256",
    "Common Name (CN)" : "cert_commonName",
    "subjectAltName (SAN)" : "cert_subjectAltName",
    "Issuer" : "cert_caIssuers",
    "Trust (hostname)" : "cert_trust",
    "Chain of Trust" : "cert_chain_of_trust",
    "EV cert (experimental)" : "cert_certificatePolicies_EV",
    "ETS/\"eTLS\"; visibility info" : "cert_eTLS",
    "Certificate Validity (UTC)" : "cert_expirationStatus",
    "Certification not before" : "cert_notBefore",
    "Certification not after" : "cert_notAfter",
    "# of certificates provided" : "certs_countServer",
    "Certificate list ordering problem" : "certs_list_ordering_problem",
    "Certificate Revocation List" : "cert_crlDistributionPoints",
    "OCSP URI" : "cert_ocspURL",
    "OCSP stapling" : "OCSP_stapling",
    "OCSP must staple extension" : "cert_mustStapleExtension",
    "DNS CAA RR (experimental)" : "DNS_CAArecord",
    "Certificate Transparency" : "certificate_transparency"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
HTTP_TEST = {
    "HTTP Status Code" : "HTTP_status_code",
    "HTTP clock skew" : "HTTP_clock_skew",
    "Strict Transport Security" : "HSTS",
    "Public Key Pinning" : "HPKP",
    "Server banner" : "banner_server",
    "Application banner" : "banner_application",
    "Cookie Secure flag" : "cookie_secure",
    "Cookie HTTPOnly flag" : "cookie_httponly",
    "X-Frame-Options" : "X-Frame-Options",
    "X-Content-Security-Policy" : "X-Content-Security-Policy",
    "Cache-Control" : "Cache-Control",
    "Pragma" : "Pragma",
    "Reverse Proxy banner" : "banner_reverseproxy"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
VULN_TEST = {
    "Heartbleed (CVE-2014-0160)" : "heartbleed",
    "CCS (CVE-2014-0224)" : "CCS",
    "Ticketbleed (CVE-2016-9244) experiment" : "ticketbleed",
    "ROBOT" : "ROBOT",
    "Secure Renegotiation (RFC 5746)" : "secure_renego",
    "Secure Client-Initiated Renegotiation" : "secure_client_renego",
    "CRIME; TLS (CVE-2012-4929)" : "CRIME_TLS",
    "BREACH (CVE-2013-3587)" : "BREACH",
    "POODLE; SSL (CVE-2014-3566)" : "POODLE_SSL",
    "TLS_FALLBACK_SCSV (RFC 7507)" : "fallback_SCSV",
    "SWEET32 (CVE-2016-2183; CVE-2016-6329)" : "SWEET32",
    "FREAK (CVE-2015-0204)" : "FREAK",
    "DROWN (CVE-2016-0800; CVE-2016-0703)" : "DROWN",
    "LOGJAM (CVE-2015-4000) experimental" : "LOGJAM",
    "BEAST (CVE-2011-3389)" : "BEAST",
    "LUCKY13 (CVE-2013-0169) experimental" : "LUCKY13",
    "RC4 (CVE-2013-2566; CVE-2015-2808)" : "RC4"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
OPENSSL_TEST = {
    'xc030' : "cipher_xc030",
    'x9f' : "cipher_x9f",
    'xc02f' : "cipher_xc02f"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
CLIENTS_SIMULATION = {
    "Android 4.4.2" : "clientsimulation-android_442",
    "Android 5.0.0" : "clientsimulation-android_500",
    "Android 6.0" : "clientsimulation-android_60",
    "Android 7.0 (native)" : "clientsimulation-android_70",
    "Android 8.1 (native)" : "clientsimulation-android_81",
    "Android 9.0 (native)" : "clientsimulation-android_90",
    "Android 10.0 (native)" : "clientsimulation-android_X",
    "Chrome 74 (Win 10)" : "clientsimulation-chrome_74_win10",
    "Chrome 79 (Win 10)" : "clientsimulation-chrome_79_win10",
    "Firefox 66 (Win 8.1/10)" : "clientsimulation-firefox_66_win81",
    "Firefox 71 (Win 10)" : "clientsimulation-firefox_71_win10",
    "IE 6 XP" : "clientsimulation-ie_6_xp",
    "IE 8 Win 7" : "clientsimulation-ie_8_win7",
    "IE 8 XP" : "clientsimulation-ie_8_xp",
    "IE 11 Win 7" : "clientsimulation-ie_11_win7",
    "IE 11 Win 8.1" : "clientsimulation-ie_11_win81",
    "IE 11 Win Phone 8.1" : "clientsimulation-ie_11_winphone81",
    "IE 11 Win 10" : "clientsimulation-ie_11_win10",
    "Edge 15 Win 10" : "clientsimulation-edge_15_win10",
    "Edge 17 (Win 10)" : "clientsimulation-edge_17_win10",
    "Opera 66 (Win 10)" : "clientsimulation-opera_66_win10",
    "Safari 9 iOS 9" : "clientsimulation-safari_9_ios9",
    "Safari 9 OS X 10.11" : "clientsimulation-safari_9_osx1011",
    "Safari 10 OS X 10.12" : "clientsimulation-safari_10_osx1012",
    "Safari 12.1 (iOS 12.2)" : "clientsimulation-safari_121_ios_122",
    "Safari 13.0 (macOS 10.14.6)" : "clientsimulation-safari_130_osx_10146",
    "Apple ATS 9 iOS 9" : "clientsimulation-apple_ats_9_ios9",
    "Java 6u45" : "clientsimulation-java_6u45",
    "Java 7u25" : "clientsimulation-java_7u25",
    "Java 8u161" : "clientsimulation-java_8u161",
    "Java 11.0.2 (OpenJDK)" : "clientsimulation-java1102",
    "Java 12.0.1 (OpenJDK)" : "clientsimulation-java1201",
    "OpenSSL 1.0.2e" : "clientsimulation-openssl_102e",
    "OpenSSL 1.1.0l (Debian)" : "clientsimulation-openssl_110l",
    "OpenSSL 1.1.1d (Debian)" : "clientsimulation-openssl_111d",
    "Thunderbird (68.3)" : "clientsimulation-thunderbird_68_3_1"
}

# { (Value in results csv from TESTSSL) : (Value in results csv from TESTSSL)}
TESTSSL_INFO={ 
    'Testing protocols via sockets except NPN+ALPN': SOCK_INFO,
    'Testing cipher categories': CIPHERS_TEST,
    'Testing robust (perfect) forward secrecy': FORWARD_SECRECY,
    'Testing server preferences': SERVER_PREFERENCES,
    'Testing server defaults (Server Hello)': SERVER_DEFAULT,
    'Testing HTTP header': HTTP_TEST,
    'Testing vulnerabilities': VULN_TEST,
    'Testing 370 ciphers via OpenSSL plus sockets against the server; ordered by encryption strength': OPENSSL_TEST,
    'Running client simulations (HTTP) via sockets': CLIENTS_SIMULATION
}

def parse_testssl_csv(files_folder, current_time):
    global HEADERS
    global RESOLVED_HEADERS
    global TESTSSL_INFO

    #Write results on an output CSV file
    with open(f'results_{current_time}.csv', 'w') as wf:
        #Domain column name
        wf.write('Host,')
        HEADERS=[]
        RESOLVED_HEADERS =[]

        #Write column names row in results CSV file
        for title in TESTSSL_INFO:
            for k in TESTSSL_INFO[title]:
                wf.write(f'{k},')
                HEADERS.append(k)
                RESOLVED_HEADERS.append(TESTSSL_INFO[title][k])
        
        wf.write('\n')

        csv_files = [x for x in os.listdir(files_folder) if os.path.splitext('my_file.txt')[1]=='.csv']

        #For each TESTSSL csv file in input folder
        with alive_bar(len(csv_files)) as bar:
            for filename in os.listdir(files_folder):
                INFO_DICT={}
                
                domain = filename.split('_')[0]
                replaced_content = []

                #Read each line, remove spaces and " and split w.r.t. commas
                with open(os.path.join(files_folder, filename), 'r') as f:
                    content = f.readlines()
                    lines= [x.replace(' ', '').replace('"', '').replace('\n','').split(',') for x in content]

                count=0
                id_name = -1
                id_severity = -1
                
                #Parse headers row (row with column names)
                for x in lines[0]:
                    if x=='id':
                        id_name = count

                    elif x=='severity':
                        id_severity = count
                    
                    count+=1

                #Read otherlines and store their values
                for i in range(1,len(replaced_content)):
                    if replaced_content[i][id_name] in RESOLVED_HEADERS:
                        for j in range(len(RESOLVED_HEADERS)):    
                            if RESOLVED_HEADERS[j]==replaced_content[i][id_name]:
                                INFO_DICT[HEADERS[j]] = replaced_content[i][id_severity]
                    
                #Write TESTSSL in final results CSV file
                wf.write(f'{domain},')
                for k in HEADERS:
                    try:
                        wf.write(f'{INFO_DICT[k]},')
                    except KeyError:
                        wf.write(',')

                wf.write('\n')

                bar()

def input_parameters():
    """
    Parse command line parameters.

    Return
    ----------
    csv_folder (str): Path of the folder with all the TESTSSL CSV files.
    """    
    
    #Define argument parser
    parser = argparse.ArgumentParser()

    #Create command line arguments
    parser.add_argument('--csv-folder', '-csv', dest='csv_folder', help='Path of the folder with all the TESTSSL CSV files.')
    
    #Parse command line arguments
    args = parser.parse_args()

    #Ask user input folder if invalid as command line argument
    csv_folder = ''
    
    while csv_folder=='' or (not os.path.isdir(csv_folder)):    
        cprint('___CSV folder___', 'blue')
        ip_file = input()
    
    return csv_folder

def main():
    #Read command line arguments (Folder with TESTSSL CSV files)
    csv_folder = input_parameters()
    
    #Current time
    now = datetime.now()
    current_time = now.strftime("%Y%m%d")

    #Parse input CSV files
    parse_testssl_csv("CSV", current_time)

if __name__=="__main__":
    main()