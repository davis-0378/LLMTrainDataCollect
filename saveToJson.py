import json
import os

class saveToJson:
    def __init__(self) -> None:
        self.data = []

    # 用來檢查抓出來的資料 => JSON格式
    def printResult(self):
        print(self.data)

    def appendData(self, message, star):
        self.data.append({"message": message, "starNumber": star})
        #self.printResult()

    def save_text_to_file(self, directory, filename):
        """
        將儲存好的內容轉變為JSON格式並存入指定目錄。
        
        :param directory: 要儲存檔案的目錄路徑
        :param filename: 儲存檔案的名稱（包含副檔名，如 "data.json"）
        """
        # 確保目錄存在
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 完整的檔案路徑
        file_path = os.path.join(directory, filename)

        # 將資料轉換為 JSON 格式的字串
        json_data = json.dumps(self.data, ensure_ascii=False, indent=4)
        
        #self.printResult()
        try:
            # 將 JSON 資料寫入檔案
            with open(filename, "w", encoding="utf-8") as file:
                file.write(json_data)
            print(f"資料已成功儲存至 {file_path}")
        except Exception as e:
            print(f"儲存檔案時發生錯誤: {e}")

            

