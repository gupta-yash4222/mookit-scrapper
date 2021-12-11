import getpass

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://hello.iitk.ac.in/user/login")

userElem = browser.find_element_by_id('edit-name')
passElem = browser.find_element_by_id('edit-pass')

username = input("Enter your IITK username")
userpass = getpass.getpass()
course = input("Enter the course id").lower()

userElem.send_keys(username)
passElem.send_keys(userpass)
passElem.submit()

browser.get('https://hello.iitk.ac.in/course/' + course)
linkElem = browser.find_element_by_css_selector("input[value='Access Course']")
linkElem.submit()

noteElems = browser.find_elements_by_css_selector("a[title='splitResourcesData.altText']")

download_dir = "/Users/apple/Downloads"
options = webdriver.ChromeOptions()

options.add_experimental_option(
    'prefs',
    {
        "download.default_directory": "/Users/apple/Desktop/Personal_Stuff/CS345A",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

print("Downloading the notes")

for noteElem in noteElems:
    noteURL = noteElem.get_attribute('href')

    if '.pdf' in noteURL:
        print(noteURL.split('?')[0])
        driver.get(noteURL.split('?')[0])
    else:
        print(noteURL.split('?')[0])
        driver.get(noteURL.split('?')[0])

print("Downloaded the notes")

import time
time.sleep(10)