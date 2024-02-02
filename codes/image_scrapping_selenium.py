import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import urllib

food_list = {
    'momos' : 100,
    'dalbhat' : 100,
    'selroti' : 100
    }

for food, n in food_list.items():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/Nirajan/AppData/Local/Google/Chrome/User Data/Default')
    driver = uc.Chrome(options=options)
    driver.minimize_window()

    url = str(f'https://www.google.com/search?sca_esv=3cbe9f3cb5d0638a&sxsrf=ACQVn08s6Q6kamb4wJ51lyk25b7qXWtKmQ:1706887592475&q={food}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjszPvk-4yEAxUZSGwGHWIlDc8Q0pQJegQIEhAB&biw=1536&bih=730&dpr=1.25')
    driver.get(url)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)
    j = n//30
    for i in range(j):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)

    img_results = driver.find_elements(By.XPATH, "//img[contains(@class, 'Q4LuWd')]")

    image_urls = []
    for img in img_results:
        image_urls.append(img.get_attribute('src'))

    file_name = food.replace('+', '_')
    folder_path = f'./dataset/{file_name}/'

    for i in range(n):   
        urllib.request.urlretrieve(str(image_urls[i]), f"{folder_path}{i}.jpg")

    driver.quit()
    time.sleep(3)
