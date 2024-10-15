#######################
# @author: RaffaDNDM
# @date:   2022-09-25
#######################

from copy import deepcopy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from datetime import datetime
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from urllib import parse
import shutil
import requests
import matplotlib.pyplot as plt
from termcolor import colored

# HTTP Proxy to redirect traffic to Burp Suite
'''
proxy = '127.0.0.1:8080'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['REQUESTS_CA_BUNDLE'] = "./certificate.pem" #PEM file generated from Burp Suite certificate
'''

# Output folder with results
output_folder='results'+datetime.now().strftime("%Y%m%d-%H_%M_%S")
# Output folder for images to be consulted without HTML
output_images=os.path.join(output_folder, 'images')
# Output folder for HTML resources
output_html= os.path.join(output_folder, "html")

# Input file with target URLs
input_file='targets.txt'

# Create output folder for results
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Create output folder for results
if not os.path.exists(output_images):
    os.mkdir(output_images)

# Clone template folder with HTML default resources
shutil.copytree('template', output_html)

# Selenium driver initialization
chrome_options = Options()
# Don't open the browser to take the screenshot
chrome_options.add_argument('--headless')
# Set proxy
#chrome_options.add_argument(f'--proxy-server={PROXY}')
# Set size of all screenshots
chrome_options.add_argument("--window-size=1920x1080")
# Initialize Selenium driver and download the last version
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

# Dictionary with information for all target URLs
URLs_info = {}
# Single information for a single target URL
INFO = { 'URL' : '',
    'Code' : '',
    'Absolute Path' : '',
    'Relative Path' : ''
}
# Dictionary with response code as key and list of infos as value:
# - the list contains (URL, Screenshot path) couples for each URL with that response code
CODES = {}

# Read input file with target URLs
with open(input_file, 'r') as rf:
    targets = [x.replace("\n", "") for x in rf.readlines()]

# Number of target URLs to be tested
num_targets = len(targets)

# Test target URLs
with alive_bar(num_targets, title=colored(f'Screenshots', 'blue')) as bar:
    
    # For each target URL
    for t in targets:
        # Parse domain & scheme from URL
        URL_parsed = parse.urlparse(t)
        domain = URL_parsed.netloc
        scheme = URL_parsed.scheme
        bar.text(colored(t, 'yellow'))

        if not (domain in URLs_info):
            URLs_info[domain] = []

        # Create a folder for each domain in 'images' folder, where screenshots will be stored
        if not os.path.exists(os.path.join(output_images, domain)):
            os.mkdir(os.path.join(output_images, domain))

        # Create a folder for each domain in 'images' folder, where screenshots for HTML will be stored
        if not os.path.exists(os.path.join(output_html, 'images', domain)):
            os.mkdir(os.path.join(output_html, 'images', domain))
        
            # Request with selenium
            driver.get(t)
            # HTTP request with requests to analyse response code
            status_code = requests.get(t).status_code

            # Path, starting from current directory, of the screenshot for HTML that will be stored
            absolute_path = os.path.join(output_html, 'images', domain, f'{len(URLs_info[domain])+1}_{status_code}.png')
            # Path, starting from current directory, of the screenshot that will be stored
            relative_path = os.path.join('images', domain, f'{len(URLs_info[domain])+1}_{status_code}.png')
        
        # Create URL information instance (cloning the template one)
        info = deepcopy(INFO)
        # Insert info related to URL
        info['URL'] = t
        info['Code'] = str(status_code)
        info['Absolute Path'] = absolute_path
        info['Relative Path'] = relative_path
        URLs_info[domain].append(info)

        # Create dictionary instance for a new response code
        if not (str(status_code) in CODES):
            CODES[str(status_code)]=[]

        # Store URL with response code 'status_code' and path to screenshot image in 
        CODES[str(status_code)].append((t,relative_path))

        # Save the screenshot of target URL for HTML
        driver.save_screenshot(absolute_path)
        
        # Read the screenshot of target URL as a PNG image
        png = driver.get_screenshot_as_png()
        
        # Add URL as text box in the image
        img = Image.open(BytesIO(png))
        w,h = img.size
        d = ImageDraw.Draw(img)
        fontsize=30
        font = ImageFont.truetype("arial.ttf", fontsize)
        #bbox=d.textbbox((10,h-50), t, font=font)
        #d.rectangle(bbox, fill="black")
        d.text((10,h-50), t, fill=(255,0,0), font=font)
        # Store the screenshot of target URL, with highlighted target URL on the image, in 'images' folder
        img.save(os.path.join(output_images, domain, f'{len(URLs_info[domain])}_{status_code}.png'))
        
        # Upgrade counter of processed URLs
        bar()


with open(os.path.join('template', 'index.html'), 'r') as f_results, \
     open(os.path.join('template', 'domains.html'), 'r') as f_domains, \
     open(os.path.join('template', 'status-codes.html'), 'r') as f_codes, \
     open(os.path.join(output_html, 'index.html'), 'w') as out_results, \
     open(os.path.join(output_html, 'domains.html'), 'w') as out_domains, \
     open(os.path.join(output_html, 'status-codes.html'), 'w') as out_codes:
    
    #Read content
    html_results = f_results.read()
    html_domains = f_domains.read()
    html_codes = f_codes.read()
    #Parse html content
    soup_results = BeautifulSoup(html_results, "html.parser")
    soup_domains = BeautifulSoup(html_domains, "html.parser")
    soup_codes = BeautifulSoup(html_codes, "html.parser")

    # Scan the list of unique response codes, returned from all target URLs (sorted)
    for code in sorted(CODES):
        ###################################
        #          Navigation bar         #
        ###################################    
        nav_codes=soup_results.find(id="nav_codes")
        #<a href="#400">401</a>
        nav_code=soup_results.new_tag("a", attrs={"href": f'status-codes.html#{code}'})
        nav_code.append(code)
        nav_codes.append(nav_code)

        nav_codes=soup_domains.find(id="nav_codes")
        #<a href="#400">401</a>
        nav_code=soup_domains.new_tag("a", attrs={"href": f'status-codes.html#{code}'})
        nav_code.append(code)
        nav_codes.append(nav_code)

        nav_codes=soup_codes.find(id="nav_codes")
        #<a href="#400">401</a>
        nav_code=soup_codes.new_tag("a", attrs={"href": f'#{code}'})
        nav_code.append(code)
        nav_codes.append(nav_code)

        ###################################
        #           Status codes          #
        ################################### 

        # List of (URL, Screenshot path) related to current statu code
        img_infos = CODES[code]
        
        # Section title for each response code
        #<h1>200</h1>
        title = soup_codes.new_tag("h1", attrs={'id' : code})
        title.append(code)

        # Gallery div for each response code section
        '''
        <div class="gallery">
            ...
        </div>
        '''
        div = soup_codes.new_tag("div", attrs={'class': 'gallery'})

        # For each (URL, Screenshot Path) couple
        for info in img_infos:
            URL,relative_path = info
            # Create gallery screenshot entry for the URL with current response code 
            '''
            <div class="gallery">
                <a href="results20220918/www.google.com/_HTTP.png" data-lightbox="mygallery"><img src="results20220918/www.google.com/_HTTP.png" width="20%" height="auto"></a>
                <a href="results20220918/www.google.com/_HTTPS.png" data-lightbox="mygallery"><img src="results20220918/www.google.com/_HTTPS.png" width="20%" height="auto"></a>
            </div>
            '''
            a = soup_codes.new_tag("a", attrs={'href': relative_path, 'data-lightbox':'mygallery', 'data-title' : URL})
            img = soup_codes.new_tag("img", attrs={'src': relative_path, 'width': '20%', 'height' : 'auto'})
            a.append(img)
            div.append(a)
        
        # Add the title and the gallery of the current response code to status code web page
        soup_codes.html.body.append(title)
        soup_codes.html.body.append(div)

    # For each unique target domain
    for domain in sorted(URLs_info):
        ############################################
        #              Domain section              #
        ############################################

        # Title with current domain
        #<h1>www.google.com</h1>
        title = soup_domains.new_tag("h1")
        title.append(domain)
        
        # Gallery div for each domain section
        '''
        <div class="gallery">
            ...
        </div>
        '''
        div = soup_domains.new_tag("div", attrs={'class': 'gallery'})

        # For each dictionary entry related to URLs of current domain
        for info in URLs_info[domain]:
            # Create gallery screen entry for the URL with current response code 
            '''
            <div class="gallery">
                <a href="results20220918/www.google.com/_HTTP.png" data-lightbox="mygallery"><img src="results20220918/www.google.com/_HTTP.png" width="20%" height="auto"></a>
                <a href="results20220918/www.google.com/_HTTPS.png" data-lightbox="mygallery"><img src="results20220918/www.google.com/_HTTPS.png" width="20%" height="auto"></a>
            </div>
            '''
            a = soup_domains.new_tag("a", attrs={'href': info['Relative Path'], 'data-lightbox':'mygallery', 'data-title' : f"{info['URL']}<br><b>{info['Code']}<b>"})
            img = soup_domains.new_tag("img", attrs={'src': info['Relative Path'], 'width': '20%', 'height' : 'auto'})
            a.append(img)
            div.append(a)

        # Add the title and the gallery of the current domain to domains web page
        soup_domains.html.body.append(title)    
        soup_domains.html.body.append(div)

    
    ############################################
    #               Plot section               #
    ############################################
    # List with number of URLs with specific response code (for each response code)
    values = [len(x) for x in CODES.values()]
    
    # Create the summary bar graph (number of responses for each response code)
    #<h1>Resume</h1>
    title = soup_results.new_tag("h1")
    title.append("Resume")
    plt.bar(CODES.keys(), values, width=0.2)
    plt.ylabel('Number of responses', fontsize=14)
    plt.xlabel('Codes', fontsize=14)
    plt.yticks(range(max(values)+1))
    plt.savefig(os.path.join(output_folder, "images", f"plt_codes.png"))
    plt.savefig(os.path.join(output_folder, "html", "images", f"plt_codes.png"))
    plt.close()

    # Store the bar graph as a PNG image
    img = soup_results.new_tag("img", attrs={'src': os.path.join("images", f"plt_codes.png"), 'width': '40%', 'height' : 'auto'})
    # Add the image to home results web page
    soup_results.html.body.append(title)
    soup_results.html.body.append(img)

    # Create a bar graph for each response code (number of responses with a response code for each domain)
    #<h1>Response codes</h1>
    title = soup_results.new_tag("h1")
    title.append("Responses codes")
    soup_results.html.body.append(title)
    
    # For each unique response code, returned from all target URLs (sorted)
    for code in CODES:
        plt_info = {}

        # For each domain
        for domain in URLs_info:
            info_list = URLs_info[domain]
            count=0

            for x in info_list:
                if x["Code"] == code:
                    count+=1

            # Store the number of URLs with current response code and domain
            plt_info[domain]=count

        # Create the bar graph for current response code with number of responses for each domain
        plt_info = {k: plt_info[k] for k in sorted(plt_info)}
        plt.barh(list(plt_info.keys()), list(plt_info.values()))
        plt.title(code)
        plt.xlabel('Number of responses', fontsize=14)
        plt.xticks(range(max(list(plt_info.values()))+1))
        plt.savefig(os.path.join(output_folder, "images", f"plt_{code}.png"))
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, "html", "images", f"plt_{code}.png"))
        plt.close()

        '''
        <div class="gallery">
            <img src="images/plt_codes.png" width="40%" height="auto">
        </div>
        '''
        # Store the bar graph as a PNG image
        img = soup_results.new_tag("img", attrs={'src': os.path.join("images", f"plt_{code}.png"), 'width' : "40%", 'height' : "auto"})
        # Add the image to home results web page
        soup_results.html.body.append(img)

    # Save changes of all results HTML pages 
    out_results.write(str(soup_results))
    out_domains.write(str(soup_domains))
    out_codes.write(str(soup_codes))