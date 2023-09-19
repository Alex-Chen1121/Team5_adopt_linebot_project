import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

options = Options()
options.chrome_executable_path = r"C:\Users\09379\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(options=options)

driver.get("https://wepet.tw/%E5%AF%B5%E7%89%A9%E9%A0%98%E9%A4%8A")

# Wait for the dropdown element to appear and select the value "貓"
wait = WebDriverWait(driver, 2)
dropdown = wait.until(EC.presence_of_element_located((By.ID, "animal")))
select = Select(dropdown)
select.select_by_value("貓")

# Click on the search button
search_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][class='btn btn-info btn-sm text-white'][value='搜尋']")
search_button.click()

# Loop through multiple pages
data_list = []
page_number = 1
while True:
    print(f"======================== Page {page_number} ========================")

    # Get the "詳細" links on the current page
    links = driver.find_elements(By.LINK_TEXT, "詳細")

    # Loop through the "詳細" links on the current page
    for link in links:
        link_url = link.get_attribute("href")
        print("網址:", link_url)

        # Open the "詳細" page in a new tab and switch to the new tab
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link_url)

        # Wait for the image element to appear
        wait = WebDriverWait(driver, 5)
        image_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "img-fluid")))

        # Get the image URL from the "src" attribute of the image element
        image_url = image_element.get_attribute("src")
        print("照片:", image_url)

        # Perform some actions here if needed
        name = driver.find_element(By.CLASS_NAME, "product-single").text
        print("名字:", name)

        tags = driver.find_elements(By.CLASS_NAME, "col-12.mb-1")
        for tag in tags:
            print(tag.text)
            break

        # Append the data to the list
        data_list.append({
            "網址": link_url,
            "照片": image_url,
            "名字": name,
            "標籤": tags[0].text if tags else None
        })

        # Close the current tab
        driver.close()

        # Switch back to the main tab
        driver.switch_to.window(driver.window_handles[0])

    # Increment the page number for the next iteration
    page_number += 1

    # Go to the next page if available, otherwise exit the loop
    try:
        next_button = driver.find_element(By.LINK_TEXT, "›")
        next_button.click()
    except:
        print("No more pages. Exiting the loop.")
        break

# Close the driver and quit the browser
driver.quit()

# Write the data_list to a JSON file
with open("pet_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)