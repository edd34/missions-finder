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
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime


load_dotenv()

result = []
col_names = [
    "lieu",
    "duree",
    "tarif",
    "teletravail",
    "debut",
    "description",
    "date",
    "link",
]
my_df = pd.DataFrame(columns=col_names)
options = Options()
options.headless = True
driver = webdriver.Firefox(
    options=options, service=Service(GeckoDriverManager().install())
)


def handler(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    my_df.to_csv("report_file.csv", sep=";", encoding="utf-8")
    driver.close()
    exit(0)


driver.get("https://www.freelance-info.fr/login-page.php")

username_elem = driver.find_element(by=By.ID, value="_username")
password_elem = driver.find_element(by=By.ID, value="_password")

username_elem.clear()
password_elem.clear()

username_elem.send_keys(os.getenv("USERNAME"))  # email freelance-info
password_elem.send_keys(os.getenv("PASSWORD"))  # mot de passe freelance-info
password_elem.send_keys(Keys.RETURN)

list_keywords = ["développeur", "python", "flask", "django", "backend", "test"]
mandatory_keywords = ["python", "django", "flask"]
param_keyword = ",".join(list_keywords)
current_page = 1
driver.get(
    "https://www.freelance-info.fr/missions?keywords=" + param_keyword + "&page=1"
)
nb_total_page = (
    max(
        [
            int(word)
            for word in driver.find_element(by=By.ID, value="mission2").text.split()
            if word.isdigit()
        ]
    )
    / 10
)
signal(SIGINT, handler)

for page in tqdm(range(1, ceil(nb_total_page))):
    print(page)
    driver.get(
        "https://www.freelance-info.fr/missions?keywords="
        + param_keyword
        + "&page="
        + str(page)
    )
    pagination_xpath = "/html/body/div[2]/main/div/div/div[1]/nav/ul"
    list_pagination = driver.find_element(
        by=By.XPATH, value=pagination_xpath
    ).find_elements(by=By.XPATH, value="./*")

    list_offers = driver.find_elements(by=By.ID, value="offre")
    link_list = [
        offer.find_element(
            by=By.CSS_SELECTOR, value=".rtitre.filter-link"
        ).get_attribute("href")
        for offer in list_offers
    ]
    for link in link_list:
        driver.get(link)
        abstract = driver.find_element(by=By.CSS_SELECTOR, value=".col-8.left")
        list_abstract_content_line = abstract.text.split("\n")
        list_abstract_content_split = [
            elem.split(":") for elem in list_abstract_content_line
        ]
        payload = {}
        payload["title"] = driver.find_element(
            by=By.CLASS_NAME, value="title-grand"
        ).text
        payload["lieu"] = list_abstract_content_split[0][1].strip()
        payload["duree"] = list_abstract_content_split[1][1].strip()
        payload["tarif"] = list_abstract_content_split[2][1].strip()
        payload["teletravail"] = list_abstract_content_split[3][1].strip()
        payload["debut"] = list_abstract_content_split[4][1].strip()
        payload["description"] = driver.find_element(
            by=By.ID, value="description-mission"
        ).text
        payload["link"] = link
        tmp_date = driver.find_element(by=By.ID, value="publié").text.split(" ")[2]
        payload["date"] = datetime.strptime(tmp_date, "%d/%m/%Y")
        tmp_df = pd.DataFrame(columns=col_names)
        # TODO on recupere toutes les donnees puis on filtre ensuite
        my_df.loc[len(my_df)] = payload

        # if is_subseq(mandatory_keywords, [payload["description"].lower()]):
        #     print(payload["title"], payload["link"])
        #     result.append(payload)

    current_page += 1

driver.close()
# with open(
#     "report_file.txt", "w", encoding="utf-8"
# ) as output_file:  # enregistrement des resultats
#     output_file.write(pprint.pformat(result, indent=4))
my_df.to_csv("report_file.csv", sep=";", encoding="utf-8")
