import getpass
import json
from contextlib import contextmanager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stderr
            sys.stderr = old_stdout

@contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stderr

file = open("details.json")
details = json.load(file)

if len(details['username']) == 0:
    details['username'] = input("Enter your IITK username: ")
userpass = getpass.getpass()
if len(details['course']) == 0:
    details['course'] = input("Enter the course id: ").lower()

print("Downloading the files....")
print()

with suppress_stdout(), suppress_stderr():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://hello.iitk.ac.in/user/login")

    userElem = browser.find_element_by_id('edit-name')
    passElem = browser.find_element_by_id('edit-pass')

    userElem.send_keys(details['username'])
    passElem.send_keys(userpass)
    passElem.submit()

    browser.get('https://hello.iitk.ac.in/course/' + details['course'])
    linkElem = browser.find_element_by_css_selector("input[value='Access Course']")
    linkElem.submit()

    noteElems = browser.find_elements_by_css_selector("a[title='splitResourcesData.altText']")

    options = webdriver.ChromeOptions()

    options.add_experimental_option(
        'prefs',
        {
            "download.default_directory": details['download_dir'],
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
    )
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    for noteElem in noteElems:
        noteURL = noteElem.get_attribute('href')

        if '.pdf' in noteURL:
            print(noteURL.split('?')[0])
            driver.get(noteURL.split('?')[0])
        else:
            print(noteURL.split('?')[0])
            driver.get(noteURL.split('?')[0])

    import time
    time.sleep(6)

print("Downloaded the files...")
