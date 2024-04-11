from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service

# code to ignore browser notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
from selenium.webdriver.support.wait import WebDriverWait

service = Service(executable_path="./chromedriver.exe")
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

# open the webpage
driver.get("https://wwww.facebook.com/")

# target username
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
)
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']"))
)

# enter username and password
username.clear()


username.send_keys("sid55maurya@gmail.com")
password.clear()
# use your username and password
password.send_keys("Fullpower@69")

# target the login button and click it
time.sleep(5)
button = (
    WebDriverWait(driver, 5)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    .click()
)

# We are logged in!
print("Logged in")


# program to parse user name who posted comment
def Nameparse():
    driver.get(url)
    names = driver.find_elements_by_tag_name("h3")
    for name in names:
        name = name.text
        if name == "Narendra Modi":  # Omitting Narendra modi name from parsed list
            continue
        Name.append(name)


# program to parse comments
def Commentparse():
    driver.get(url)
    comments = (
        driver.find_elements_by_css_selector("[class='ed']")
        or driver.find_elements_by_css_selector("[class='ee']")
        or driver.find_elements_by_css_selector("[class='eg']")
    )
    for comment in comments:
        comment = comment.text
        Comment.append(comment)


# Program to scrap comments from each page
Name = []
Comment = []
cnt = 0
# program to parse comments from 5 pages, if you want comments from all pages then use while loop
for i in range(6):
    # while True:
    url = "https://mbasic.facebook.com/story.php?story_fbid=pfbid02feJVRoJrAhshuK51SzJakDru9uSCmpqw5JKcYfVZne1oVFpW7WzQbjMYsX5gB1szl&id=100064681269092&eav=AfYRaKD9FxxkZzTWKXJnIEe0dXbPLiGAQ3ofsKalz8is47pfgPcXBpDzdOlprooXt2Y&refid=17&_ft_=encrypted_tracking_data.0AY8OVF5Wsnv2QF9CV2-0TX_OOv-dKBnVpqScjgO_M_XCLNb-dEuLHgQnxxJeXjdc1MTe7H_GhHeC-ZhUEWTP0KYox0lUgHYEDVmJ16jCSFO8vN3omLT3Wp4qXZ4WuiL2mC6XKgzWVkPE8wU3Lqdr59NQHzIG009f48SbB7Cg_XqfEtswq1UWoBxc5ErmD2nU1nGvg9e8krwU-Lbg7FnQZo6TmEah58lmlXlJAg_neveSA9Ea4KOSv3_fKcpHzDghflaC287SfpuZfvIPoFWMJfGVMq_gOUbkdiYmkxmdcIROXZrvGH_0eUeEO9qL5bwpr5ep8S9qYkPIJIcROa9ieBhw9KIx0R4q98UXHoobOJJnT8Hhfcs6JDjIbRdd_glGdc5Crxd-v6WN8yVGpJUsZZL7Vm1CxYNFEKyIirGcih18V3_iBwirsMpv1c8suYjOvEWGOI2UNIUh1-XDm-7TrhgKx4p0e7bUq7AYV63P2MuTNd7VqsbhhCL_Dc0brQlESe0gqHrngqLmHijhbcLxn6G_at9JpKiZ1tPmCjYrIZztWwOob3Rca-8lqo-oghu7yOsETRrz-_0hwQY2r1Gpp_3EwBkwdzsCMlMQ3UM7VFpc3_AaXTdSY1MozRfDbpLLIw2adA_MX0opVJzCXJzMOs_Xq6OT0tUUbClYBXDXFsAQmMIYeW9wtawz5gYhoxkVyDKsJaYQAU_Ess4b1_eK1oibaUH0y_G5QN807GkTTVfTxXpRGzEu6rfTw5ztc0l51itTN0wG9wsRaG36Blr_Y2zmHm9Q4zMHxTHKug-ZktZUi10dQVeLEJ5IkFAtrt-TfOuzDhq_qEj6gUFVEvr31PYlG1xH2Dcv1Ms4qOvwSMfdomQW2JSjOaCTEOCd8T6AuWhbaiiC89vIgrQ7g7PHQt4AC81hVjOH_K_CJcDJYI60IL9rK00IqRIeHCn6dTHj5zYxuyWN4MuTh6RHT2DlJr8YcqG9IUq0-aGKtaDJW5LjxL6P9OCmeXiukZlv3NJsfGpbEW1d2MRc_RPdQzl8l3lrE7kgMfz_qYeiV_UVge6doKY5upwpnM3f4xazLslYksqemGjqWjs7i7ZCCoaNAYe47GbX1VC-8EJAYggq_n4AqRii7Gh9XQSbkobbUDvmXicsRwB7BKJNJEFIzSG4uyEaJkQ9OwAigqhmtnhpUKqGE-Hw695BLllWLoa4JsxTPsGv-MImxnFB0mLNBXdDYS22siYx4d6tzZXcfVxlV-6IFoffdqPzAqD7XBhcpxAJ0oVbhcFCa53lhJxIANqKKD8yuiGE_Yy_IcZv3fF6TQ4T5MvkNzYr_TB5YvJ4EgUj6h9BpIJL7GKxKxjWudRC7C4dpEJ4UXTNqNxoam4Yc722UAXULt1S1fUFSJT6HjnatpsENUYT-l73UAAoVgrTeQgz-hUK8lpIqmGCL8E4ujafCys0Vue2QAswfgVoKE0BwZYw&__tn__=%2AW-R&paipv=0#footer_action_list"
    url = url + str(cnt)
    Nameparse()
    print(Name)
    Commentparse()
    print(Comment)
    print(url)
    cnt = cnt + 10

# create a dataframe
data = pd.DataFrame({"Name": Name, "Comment": Comment})
data.to_csv("Facebbok_comments.csv")
print("data saved")

