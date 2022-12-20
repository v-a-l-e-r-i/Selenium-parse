from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import json
import time

agent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")

driver = webdriver.Chrome(
    executable_path="C:\\sers\HP\\PycharmProjects\\selenium_parser\\chromedriver.exe",
    options=options
)

films = []
marks = []
images = []
try:
    # go to site
    driver.get(url="https://hdrezka.ag/films/page/1/")
    driver.implicitly_wait(5)

    # take a number of pages and films
    page = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div[2]/div/div[1]/div[37]/a[10]')
    num = driver.find_elements(By.CLASS_NAME, "b-content__inline_item")

    # take information about films
    for x in range(0, int(page.text)):
        if x+1 <= 1:  # limitation of choice
            for i in range(30, len(num)):
                items = driver.find_elements(By.XPATH,
                                             f'//*[@id="main"]/div[4]/div[2]/div/div[1]/div[{i + 1}]/div[1]/a')
                items[0].click()
                film_title = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div[2]/div[1]/div[1]/h1')
                photo = driver.find_element(By.XPATH,
                                            '//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[1]/div/a/img')
                grade = driver.find_element(By.CLASS_NAME, 'bold')

                films.append(film_title.text)
                marks.append(grade.text)
                images.append(photo.get_attribute('src'))

                driver.get(url=f"https://hdrezka.ag/films/page/{x + 1}/")
                driver.implicitly_wait(5)
        else:
            break

except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()

sl = {}
for i in range(len(films)):
    sl = dict(zip(films, zip(marks, images)))

with open("file.json", 'w', encoding='utf-8') as file:
    json.dump(sl, file, indent=4, ensure_ascii=False)
    file.close()
