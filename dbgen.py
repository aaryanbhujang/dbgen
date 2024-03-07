from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time 
import os
from selenium.webdriver.chrome.options import Options

#lists
names = []
addresses = []
numbers = []

#banner
os.system("mode 1000")
print('\n'
'██████████   █████       █████████\n'
'░░███░░░░███ ░░███       ███░░░░░███\n'
'░███   ░░███ ░███████  ███     ░░░   ██████  ████████\n'
'░███    ░███ ░███░░███░███          ███░░███░░███░░███\n'
'░███    ░███ ░███ ░███░███    █████░███████  ░███ ░███\n'
'░███    ███  ░███ ░███░░███  ░░███ ░███░░░   ░███ ░███\n'
'██████████   ████████  ░░█████████ ░░██████  ████ █████\n'
'░░░░░░░░░░   ░░░░░░░░    ░░░░░░░░░   ░░░░░░  ░░░░ ░░░░░\n'
'                                           Author:44ry4n')




#input
location = input("Location(City):")
product = input("Product (Organic,Herbal,etc):")
dtype = input("Dealer Type(Dealers,Manufacturers,Distributors):")

#urlreq
print("\nInitializing Data Scan..\n")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--no-startup-window')
chrome_options.add_argument('--disable-dev-shm-usage')
url="https://www.justdial.com/"+location+"/"+product+"-"+dtype+"/page-1"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
driver.maximize_window()
driver.set_window_position(-10000,0)

#number converter
def strings_to_num(argument): 
    
    switcher = { 
        'dc': ' ',
        'fe': '(',
        'hg': ')',
        'ba': ' ',
        'acb': '0', 
        'yz': '1', 
        'wx': '2',
        'vu': '3',
        'ts': '4',
        'rq': '5',
        'po': '6',
        'nm': '7',
        'lk': '8',
        'ji': '9'
    } 
    
    return switcher.get(argument, "nothing")

#scrapedata
load=tqdm(total=100,position=0,leave=False)
loopnum=0
driver.execute_script("window.scrollBy(0,2000)","")
time.sleep(1)
print("Progress:",end="")
for loopnum in range(100):
    driver.execute_script("window.scrollBy(0,200)","")
    load.set_description("Retrieving...".format(loopnum))
    load.update(1)
    #print("█",end="")
    time.sleep(0.5)
load.close()
print("\nCompiling Data")
storeDetails=driver.find_elements_by_class_name('store-details')

for i in range(len(storeDetails)):
    name=storeDetails[i].find_element_by_class_name('lng_cont_name').text
    address=storeDetails[i].find_element_by_class_name('cont_sw_addr').text
    contactList=storeDetails[i].find_elements_by_class_name('mobilesv')
    myList=[]

    for j in range(len(contactList)):
        myString=contactList[j].get_attribute('class').split("-")[1]
        myList.append(strings_to_num(myString))
    names.append(name)
    addresses.append(address)
    numbers.append("".join(myList))
driver.close()
print("\nData Scraped Successfully!")
data = {'Vendor Name':names,
	    'Address':addresses,
        'Phone':numbers}
#dbgen
time.sleep(1)
print("\nGenerating Database")
df=pd.DataFrame(data)
df.to_csv(location+'_'+product+'_'+dtype+'_db.csv',mode='w',header=False)
time.sleep(0.5)
print("\nDatabase Generated! - "+location+'_'+product+'_'+dtype+"_db")
time.sleep(1)
opennow = input("\nOpen it now?(y/n):")
if opennow == 'y':
    os.system(location+'_'+product+'_'+dtype+"_db.csv")
else:
    print("Adios")
    time.sleep(0.6)
    exit()
