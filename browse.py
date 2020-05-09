from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import json

XPATH_MailingAddr = '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/div'
XPATH_ownerName = '/html/body/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div/div[2]/div'
XPATH_bldgArea = '/html/body/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/div[1]/div/div[2]/div'
XPATH_bldgCondition = '/html/body/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div[10]/div/div[2]/div'
XPATH_roofType = '/html/body/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div[13]/div/div[2]/div'
XPATH_searchbar = '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div/header/div[1]/div[1]/div[1]/div/div/div/div/input'
XPATH_firstsuggestion = '/html/body/div[3]/div/div[2]/ul/li[1]'
XPATH_detailsbox = '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/section/div[2]/div/div[1]/div[3]/a'
XPATH_errorok = '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div[2]/button'


maind_div_id = 'react-tabs-1'
properties_json = []
filename = 'austin'
direction = 'https://www.google.com/maps/search/?api=1&query='
Individual_prop = 'https://app.propstream.com/eqbackend/resource/auth/ps4/property/new/'  # + Property ID
with open(filename+'.json','r') as file:
    properties_json = json.load(file)

def login():
    global browser
    browser.get('https://login.propstream.com/')
    time.sleep(3)
    username = browser.find_element_by_xpath('//*[@id="form-content"]/form/input[1]')
    username.send_keys('username_goes_here')
    password = browser.find_element_by_xpath('//*[@id="form-content"]/form/input[2]')
    password.send_keys('password_goes_here')
    login_btn = browser.find_element_by_xpath('//*[@id="form-content"]/form/button')
    login_btn.click()
    time.sleep(3)


browser = webdriver.Chrome(ChromeDriverManager().install())
login()

try:
    proceed_btn = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[3]/button[2]')
    proceed_btn.click()
    print('logged someone else out')
    time.sleep(3)
except:
    print('already logged in')


property_data = []

for property in properties_json:
    browser.get('https://app.propstream.com/search')
    time.sleep(3)
    search_str = ''
    search_str = str(property['NUMBER']) + ' '
    search_str = search_str + str(property['STREET']) + ' '
    search_str = search_str + str(property['CITY'])

    print(search_str)

    searchbox = browser.find_element_by_xpath(XPATH_searchbar)
    while len(searchbox.get_attribute('value')) > 0:
         searchbox.send_keys(Keys.BACK_SPACE);
    searchbox.send_keys(search_str)

    time.sleep(1)

    listbox_firstsuggestion = browser.find_element_by_xpath(XPATH_firstsuggestion)
    listbox_firstsuggestion.click()
    
    time.sleep(1)

    address_found = False

    ## add case where search produces a list for the same address

    try:
        detailsbox_btn = browser.find_element_by_xpath(XPATH_detailsbox)
        temp_url = detailsbox_btn.get_attribute('href')
        detailsbox_btn.click()
        browser.get(temp_url)
        address_found = True
        print('address available')
    except:
        print('address not found')


    if address_found:
        try:
            MailingAddr = browser.find_elements_by_xpath(XPATH_MailingAddr)
            if len(MailingAddr) > 0:
                MailingAddr = MailingAddr[0].text
                print('MailingAddr Straight: ' + str(MailingAddr))
                print('Mailing Addr with 0: ' + str(MailingAddr))
        except:
            print('')