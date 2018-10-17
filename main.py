from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

import logging

df = pd.read_csv('concatenate.csv')

driver = webdriver.Chrome(executable_path='/home/skillup/skillup/sylvainer/chromedriver')

SLEEP = 0.5
KEYWORD = 'concatenate'

def get_extra_info(driver):
    try:
        sites = driver.find_element_by_xpath('//span[@class="icon icon-lien"]/following-sibling::span').text
    except Exception:
        sites = ''
    try:
        naf = driver.find_element_by_xpath('//div[@class="table-row naf"]/span[@class="valeur"]').text
    except Exception:
        naf = ''
    try:
        employees = driver.find_element_by_xpath('//div[@class="table-row effectif"]/span[@class="valeur"]').text
    except Exception:
        employees = ''

    return {
        'sites': sites,
        'naf': naf,
        'employees': employees,
    }


def get_info(keyword):
    driver.get("https://www.bing.com/")

    elem = driver.find_element_by_class_name("b_searchbox")

    # elem.clear()
    elem.send_keys(f'site:pagesjaunes.fr {keyword}')

    # time.sleep(SLEEP)
    elem.send_keys(Keys.RETURN)

    time.sleep(SLEEP)

    driver.find_element_by_xpath('//*[@id="b_results"]/li/div[1]/h2/a').click()

    time.sleep(SLEEP)

    #import ipdb; ipdb.set_trace()

    driver.find_element_by_xpath("//*[contains(text(), 'Afficher le')]/parent::a").click()

    time.sleep(SLEEP)

    divs = driver.find_elements_by_xpath('//span[@class="num-tel-label" and contains(., "tél")]/following-sibling::span[1]')

    telephones = [div.text for div in divs]

    extra_info = get_extra_info(driver)
    
    return {
        **{
            'keyword': keyword,
            'telephones': telephones,
            'url': driver.current_url,
        },
        **extra_info
    }


data = []

print('Processing {} keywords'.format(len(df)))

for keyword in df[KEYWORD]:
    try:
        info = get_info(keyword)
        data.append(info)
        print(info)
    except Exception:
        logging.exception('Failed to extract keyword: {}'.format(keyword))


data_df = pd.DataFrame(data)

data_df.to_csv('output.csv', index=False)

driver.close()