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
try:
    close_button = driver.find_element(By.XPATH, '//button[@title="Close"]')
    close_button.click()
except Exception as e:
    print(str(e))

#Connection to Database
con = duckdb.connect(database='webscrapedb.db', read_only=False)
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS delegate_info (Name VARCHAR, Job_Title VARCHAR, Organization VARCHAR, What_are_you_working_on_in_the_field_of_social_and_economic_justice VARCHAR, What_do_you_need_from_the_Delegate_community_to_move_this_work_forward VARCHAR, What_are_you_able_and_willing_to_contribute_to_the_Delegate_community VARCHAR)')


driver.implicitly_wait(10)
iframe_container = driver.find_element(By.TAG_NAME, 'iframe')
sublink = iframe_container.get_attribute('data-src');
driver.switch_to.frame(iframe_container)
a_tags = driver.find_elements(By.TAG_NAME, "a")

print(len(a_tags));
links = []
for index, a_tag in enumerate(a_tags):
    print(a_tag.text)
    links.append(a_tag.text)
    try:
        a_tag.send_keys(Keys.CONTROL + Keys.RETURN)
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[1])
        #driver.implicitly_wait(200)
        WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//h2')))
        #driver.implicitly_wait(200)
        time.sleep(2)
        name = driver.find_element(By.TAG_NAME, 'h2').text
        h4_contents = driver.find_elements(By.TAG_NAME, 'h4')
        print("Name: " + name)
        job_title = ""
        organization = ""
        for content in h4_contents:
            if(job_title == ""):
                job_title = content.text
            elif(organization == ""):
                organization = content.text
            else:
                continue
        print("================================ " + job_title + " ================================ "+organization)
        divs = driver.find_elements(By.TAG_NAME, "div")
        questions = driver.find_elements(By.XPATH, "//div[@class='expandable-content__ChildrenWrapper-ui__sc-1k0xztj-3 dCtHth']")
        answers = []
        for q in questions:
            answers.append(q.text)
        print(len(answers))
        print(answers)
        # Insert data into DuckDB table
        cursor.execute("INSERT INTO delegate_info VALUES (?, ?, ?, ?, ?, ?)", (name, job_title, organization, answers[1], answers[2], answers[3]))
        driver.implicitly_wait(10)
        cursor.execute('SELECT * FROM delegate_info')
        result = cursor.fetchall()
        print(result)
        # Close the current window
        driver.close()
        
        # Switch back to the original window
        driver.switch_to.window(driver.window_handles[0])
        a_tag = driver.find_elements(By.TAG_NAME, "a")[index]
    except StaleElementReferenceException:
        # Re-fetch a_tag in case of a stale element
        a_tag = driver.find_elements(By.TAG_NAME, "a")[index]
        print(a_tag.text)

    

# Retrieve data from DuckDB table
cursor.execute('SELECT * FROM delegate_info')
result = cursor.fetchall()
print(result)

# Close the web driver
driver.quit()
con.close()
