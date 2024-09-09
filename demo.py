from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import csv

driver = webdriver.Chrome()
driver.get("http://www.olympedia.org/statistics/medal/country")
time.sleep(10)

year = driver.find_element(By.ID, "edition_select")
gender = driver.find_element(By.ID, "athlete_gender")

year_options = year.find_elements(By.TAG_NAME, "option")
gender_options = gender.find_elements(By.TAG_NAME, "option")
usa_lst = []

for gender_option in gender_options[1:]:
    gender_option.click()
    gender_val = gender_option.text  # Corrected to gender_option.text

    for year_option in year_options[2:]:
        year_option.click()
        year_val = year_option.text  # Corrected to year_option.text
        the_soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            head = the_soup.find(href=re.compile('USA'))  # Move this inside the try block

            medal_values = head.find_all_next('td', limit=5)
            val_lst = [x.string for x in medal_values[1:]]

        except:
            val_lst = ['0' for x in range(4)]

        val_lst.append(gender_val)
        val_lst.append(year_val)

        usa_lst.append(val_lst)

with open('output.csv', 'w', newline='') as output_f:
    output_writer = csv.writer(output_f)

    for row in usa_lst:
        output_writer.writerow(row)

driver.quit()
