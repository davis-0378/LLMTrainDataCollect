# LLMTrainDataCollect

## wlecome to start :empty_nest:
![Language](https://img.shields.io/badge/language-python-brightgreen)  

### 下載程式 :heavy_check_mark:
Just [click](https://github.com/davis-0378/LLMTrainDataCollect/raw/main/CommentCollectSystem.exe)

### 遇到的問題 :fire:
> 在 Google Map 動態下滑評論的方法，這種 `driver.execute_script()` 已經沒效果了
> ```
> driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
> ```
> 所以我改成使用 ```send_keys()``` 的解法
> ```
> commentDiv = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]')
> ActionChains(driver).move_to_element(commentDiv).send_keys(Keys.END).perform()
> ```
                    
### 更新紀錄
* 2024/08/12
> #### 將儲存格式從 csv 變成 json
> 因為在評論中可能會出現','，但剛好的是 csv 用於隔開 column 之間的分隔符號恰巧是 ',' ，所以必須使用別種儲存方式。
> 因為使用 selenium 直接擷取網頁元素的關係，換行符號'\n'也會一同被扒取下來，導致資料在儲存到 json 檔案後，評論內會出現很多個'\n'，所以在爬到評論並儲存前先將'\n'這個特殊字符先從評論中剔除。
