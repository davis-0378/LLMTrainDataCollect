from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class getComment(object):
    def __init__(self, comment_number, comment_min_size, comment_max_size, essential, svjModel):
        self.comment_number = comment_number #需要的評論數量
        self.comment_min_size = comment_min_size # 每則評論的最小字數 
        self.comment_max_size = comment_max_size # 每則評論的最大字數
        self.essential = essential
        #參數設定
        self.index = 0
        self.result = ""
        #儲存模組
        self.SVJ = svjModel

    def main(self):
        # 設定Chrome選項
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # 視窗最大化
        chrome_options.add_argument("--disable-notifications")  # 禁用通知

        # 安裝ChromeDriver並啟動瀏覽器
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        try:
            # 開啟google Maps 並選擇台北市的餐廳
            driver.get("https://www.google.com/maps/search/" + self.essential)

            # 等待頁面加載（可根據需要調整時間）
            time.sleep(5)
            #                                                   //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[5]/div/a
            # 找到所有的餐廳                                    //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/div/a
            all_restaurants = driver.find_element(By.XPATH, '(//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1])')
            i = 0
            while(self.index < self.comment_number):
                # 從列表中找一個餐廳
                target = all_restaurants.find_element(By.XPATH, '(div['+ str(3 + i * 2) + ']/div/a)')
                self.getComment(target.get_attribute("href"))
                i += 1

            return True
        except Exception as e:
            print(f"發生錯誤: {e}")
        finally:
            # 關閉瀏覽器
            driver.quit()

    # 用來檢查抓出來的資料 => CSV格式
    def printResult(self):
        print(self.result)

    def getComment(self, link):
        # 設定Chrome選項
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # 視窗最大化
        chrome_options.add_argument("--disable-notifications")  # 禁用通知

        # 安裝ChromeDriver並啟動瀏覽器
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        try:
            restaurant_comment_number = 0
            # 開啟google Maps 並選擇台北市的餐廳 
            driver.get(link)

            time.sleep(1)
            divs = driver.find_elements(By.XPATH, "(//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div)")
            for div in divs:
                try:
                    if(div.find_element(By.XPATH, "div/button").get_attribute("aria-label")[0:4] == "更多評論"):
                        restaurant_comment_number = int(div.find_element(By.XPATH, "div/button").get_attribute("aria-label")[6:-1])
                        print(restaurant_comment_number) #輸出這個餐廳有多少則評論
                except Exception as e:
                    continue
            del divs

            time.sleep(1)
            #點選評論的按鈕，讓所有的評論都顯示
            commentBTN = driver.find_element(By.XPATH, "(//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2])").click()
            
            time.sleep(1)
            comments = driver.find_elements(By.XPATH, "(//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div)")
            # 找出所有評論，檢查是否可以加入訓練資料中
            for comment in comments:
                comment_text = ""
                restaurant_comment_number -= 1
                #找出評論
                if(comment.get_attribute("class") == "jftiEf fontBodyMedium "):
                    star_number = comment.find_element(By.XPATH, "div/div/div[4]/div[1]/span[1]").get_attribute("aria-label")
                    try: #看看有沒有需要展開全文，字數較多的評論會被縮起來，需要點全文的按鈕才會展開全部
                        full_comment = comment.find_element(By.XPATH, 'div/div/div[4]/div[2]/div/span[2]').click()
                    except Exception as e:
                        continue
                    comment_text = comment.find_element(By.XPATH, 'div/div/div[4]/div[2]/div/span[1]').text                          
                 
                    # 檢查這個評論的字數是否在限制範圍內 
                    if(self.comment_min_size < len(comment_text) <= self.comment_max_size):
                        self.result += comment_text + ", " + star_number[0] + "\n\n"
                        # 將資料儲存進儲存資料的元件中
                        self.SVJ.appendData(comment_text, star_number[0])
                        self.index += 1

                        print("size : " + str(len(comment_text)))
                        #print("text : " + comment_text)
                        print( str(self.comment_min_size) + " ~ " + str(self.comment_max_size))
                    
                    if(self.index >= self.comment_number):
                        break

            if(self.index < self.comment_number):
                while True:
                    # 定位到評論那排
                    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]')).perform()  
                    #動態下滑，並抓取新出現的評論
                    commentDiv = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]')
                    ActionChains(driver).move_to_element(commentDiv).send_keys(Keys.END).perform()
                    time.sleep(0.75)  # 添加适当的延迟以模拟滚动过程

                    # 把新出現的評論單獨分開，原本出現過的評論就不必再使用
                    original_comments = comments
                    print("get comments")
                    new_comments = driver.find_elements(By.XPATH, "(//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div)")
                    print("get comments successful")
                    comments = []
                    for i in range(len(new_comments) - len(original_comments), len(new_comments)):
                        comments.append(new_comments[i])
                    
                    # 從所有新出現的評論當中，檢查是否有可以加入訓練資料中的
                    for comment in comments:
                        comment_text = ""
                        restaurant_comment_number -= 1
                        #找出評論
                        if(comment.get_attribute("class") == "jftiEf fontBodyMedium "):
                            try: 
                                star_number = comment.find_element(By.XPATH, "div/div/div[4]/div[1]/span[1]").get_attribute("aria-label")

                                #看看有沒有需要展開全文，字數較多的評論會被縮起來，需要點全文的按鈕才會展開全部
                                full_comment = comment.find_element(By.XPATH, 'div/div/div[4]/div[2]/div/span[2]').click()
                                comment_text = comment.find_element(By.XPATH, 'div/div/div[4]/div[2]/div/span[1]').text
                                                        
                            
                                # 檢查這個評論的字數是否在限制範圍內 
                                if(self.comment_min_size < len(comment_text) <= self.comment_max_size):
                                    self.result += comment_text + ", " + star_number[0] + "\n\n"
                                    if '\n' in comment_text:
                                        comment_text = comment_text.replace('\n', '')
                                    # 將資料儲存進儲存資料的元件中
                                    self.SVJ.appendData(comment_text, star_number[0])
                                    self.index += 1
                                
                                    print("index : " + str(self.index))
                                #如果到需要的評論數量就結束
                                if(self.index >= self.comment_number):
                                    break
                            except Exception as e:
                                continue

                        #如果這個餐廳的評論已全部被抓出來就結束
                        if(restaurant_comment_number == 0):
                            break
                    #如果到需要的評論數量就結束
                    if(self.index == self.comment_number):
                        break
                    #如果這個餐廳的評論已全部被抓出來就結束
                    if(restaurant_comment_number == 0):
                        break
        except Exception as e:
            print(f"發生錯誤: {e}")
        finally:
            # 關閉瀏覽器
            driver.quit()
        return link