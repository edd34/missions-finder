import time
import os
import pprint
from sys import exit
from math import ceil
from signal import signal, SIGINT
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from dotenv import load_dotenv
from utils import is_subseq
load_dotenv()

result = []
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    with open("report_file.txt",'w',encoding = 'utf-8') as output_file: #enregistrement des resultats
        output_file.write(pprint.pformat(result, indent=4))
    exit(0)


driver.get("https://www.freelance-info.fr/login-page.php")

username_elem = driver.find_element_by_id("_username")
password_elem = driver.find_element_by_id("_password")

username_elem.clear()
password_elem.clear()

username_elem.send_keys(os.getenv("USERNAME")) # email freelance-info
password_elem.send_keys(os.getenv("PASSWORD")) # mot de passe freelance-info
password_elem.send_keys(Keys.RETURN)

list_keywords = ["développeur", "python", "flask", "backend", "test"]
mandatory_keywords = ["python"]
param_keyword = ",".join(list_keywords)
current_page = 1
driver.get("https://www.freelance-info.fr/missions?keywords="+param_keyword+"&page=1")
nb_total_page = max([int(word) for word in driver.find_element_by_id("mission2").text.split() if word.isdigit()])
signal(SIGINT, handler)
# while True:
for page in tqdm(range(1, ceil(nb_total_page/10))):
    print(page)
    driver.get("https://www.freelance-info.fr/missions?keywords="+param_keyword+"&page="+str(page))
    pagination_xpath = "/html/body/div[2]/main/div/div/div[1]/nav/ul"
    list_pagination = driver.find_element_by_xpath(pagination_xpath).find_elements_by_xpath('./*')

    list_offers = driver.find_elements_by_id("offre")
    link_list = [offer.find_element_by_css_selector(".rtitre.filter-link").get_attribute("href") for offer in list_offers]
    for link in link_list:
        driver.get(link)
        abstract =  driver.find_element_by_css_selector(".col-8.left")
        list_abstract_content_line = abstract.text.split('\n')
        list_abstract_content_split = [elem.split(":") for elem in list_abstract_content_line]
        payload = {}
        payload["title"] = driver.find_element_by_class_name("title-grand").text
        payload["lieu"] = list_abstract_content_split[0][1].strip()
        payload["durée"] = list_abstract_content_split[1][1].strip()
        payload["tarif"] = list_abstract_content_split[2][1].strip()
        payload["télétravail"] = list_abstract_content_split[3][1].strip()
        payload["début"] = list_abstract_content_split[4][1].strip()
        payload["description"] = driver.find_element_by_id("description-mission").text
        payload["link"] = link

        if is_subseq(mandatory_keywords, [payload["description"].lower()]):
            print(payload["title"], payload["link"])
            result.append(payload)

    # if list_pagination[-1].get_attribute("class") == "page-item active": #si derniere page atteinte, fin du programme
    #     break

    current_page += 1

driver.close()
with open("report_file.txt",'w',encoding = 'utf-8') as output_file: #enregistrement des resultats
    output_file.write(pprint.pformat(result, indent=4))
