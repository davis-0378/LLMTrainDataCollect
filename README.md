# LLMTrainDataCollect

## wlecome to statrt :empty_nest:
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
                    
