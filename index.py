from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
import duckdb


website = 'https://ocimpact.com/delegate-roster/'
driver = webdriver.Chrome()
driver.get(website)
# try:
#     close_button = driver.find_element(By.XPATH, '//button[@title="Close"]')
#     close_button.click()
# except Exception as e:
#     print(str(e))

#Connection to Database
con = duckdb.connect(database='webscrapedb.db', read_only=False)
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS delegate_info (Name VARCHAR, Job_Title VARCHAR, Organization VARCHAR, What_are_you_working_on_in_the_field_of_social_and_economic_justice VARCHAR, What_do_you_need_from_the_Delegate_community_to_move_this_work_forward VARCHAR, What_are_you_able_and_willing_to_contribute_to_the_Delegate_community VARCHAR)')


driver.implicitly_wait(10)
iframe_container = driver.find_element(By.TAG_NAME, 'iframe')
sublink = iframe_container.get_attribute('data-src');
driver.get(sublink)
a_tags = driver.find_elements(By.TAG_NAME, "a")
try:
    for index in range(0, len(a_tags), 2):
        a_tags = driver.find_elements(By.TAG_NAME, "a")  # Re-locate the elements
        a_tag = a_tags[index]

        href_attribute = a_tag.get_attribute("href")
        if href_attribute:
            driver.get(href_attribute)
            WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//h2')))
            time.sleep(2)
            
            name = driver.find_element(By.XPATH, '//h2[@class="style__Name-cmp__sc-1s7e137-1 jhjTCw"]').text
            job_title = driver.find_element(By.XPATH, "//h4[@class='style__Job-cmp__sc-1s7e137-2 dzeTcv']").text
            organization = driver.find_element(By.XPATH, '//h3[@class="style__Organization-cmp__sc-1s7e137-3 cVzOUy"]').text
            questions = driver.find_elements(By.XPATH, "//div[@class='expandable-content__ExpandableWrapper-ui__sc-1k0xztj-0 kutcyn']")
            answers = []
            for ques in questions:
                ques.find_element(By.XPATH, '//div[@class="expandable-content__ChildrenWrapper-ui__sc-1k0xztj-3 dCtHth"]')
                answers.append(ques.text)
                
            size = len(answers)
            print(size)
            while(len(answers) < 3):
               answers.append("Not Answered") #missing value
            print(answers)
            # Insert data into DuckDB table
            cursor.execute("INSERT INTO delegate_info VALUES (?, ?, ?, ?, ?, ?)", (name, job_title, organization, answers[0], answers[1], answers[2]))
            driver.implicitly_wait(10)
            # Switch back to the original window
            # driver.switch_to.window(driver.window_handles[0])
            driver.back()
            time.sleep(2)
        else:
            print("Skipped")
finally:
    # Close the web driver
    driver.quit()
    con.close()

# Retrieve data from DuckDB table
cursor.execute('SELECT * FROM delegate_info')
result = cursor.fetchall()
print(result)


