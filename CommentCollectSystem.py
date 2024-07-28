import tkinter as tk
from tkinter import filedialog, messagebox
import os
from getComment import getComment as GC
import datetime

class CommentCollectSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Comment Collect System")
        
        # Frame for inputs
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        # Comment length
        tk.Label(self.frame, text="評論最少字數:(最少為0，預設為0)").grid(row=0, column=0, sticky=tk.W)
        self.min_length = tk.Entry(self.frame)
        self.min_length.grid(row=0, column=1)
        
        tk.Label(self.frame, text="評論最多字數:(最多為100，預設為100)").grid(row=1, column=0, sticky=tk.W)
        self.max_length = tk.Entry(self.frame)
        self.max_length.grid(row=1, column=1)
        
        # The essential
        tk.Label(self.frame, text="關鍵字(預設為台北、餐廳):").grid(row=2, column=0, sticky=tk.W)
        self.essential_var = tk.Entry(self.frame)
        self.essential_var.grid(row=2, column=1)
        
        # Number of comments
        tk.Label(self.frame, text="需要多少條評論:(10~10000，預設為10)").grid(row=3, column=0, sticky=tk.W)
        self.num_comments = tk.Entry(self.frame)
        self.num_comments.grid(row=3, column=1)
        
        # Directory selection
        tk.Label(self.frame, text="選擇目錄:").grid(row=4, column=0, sticky=tk.W)
        self.dir_path = tk.Entry(self.frame, width=40)
        self.dir_path.grid(row=4, column=1)
        self.browse_button = tk.Button(self.frame, text="瀏覽", command=self.browse_directory)
        self.browse_button.grid(row=4, column=2)
        
        # The essential
        tk.Label(self.frame, text="檔案名稱(預設為 'data日期.txt' ):").grid(row=5, column=0, sticky=tk.W)
        self.fileName_var = tk.Entry(self.frame)
        self.fileName_var.grid(row=5, column=1)
        
        # Submit button
        self.submit_button = tk.Button(self.root, text="提交", command=self.submit)
        self.submit_button.pack(pady=10)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.insert(0, directory)

    def save_text_to_file(self, text, directory, filename):
        """
        將文字內容儲存為txt檔案並存入指定目錄。
        
        :param text: 要儲存的文字內容
        :param directory: 要儲存檔案的目錄路徑
        :param filename: 儲存檔案的名稱（包含副檔名，如 "output.txt"）
        """
        # 確保目錄存在
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 完整的檔案路徑
        file_path = os.path.join(directory, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"文字已成功儲存至 {file_path}")
        except Exception as e:
            print(f"儲存檔案時發生錯誤: {e}")
    
    def submit(self):
        min_length = self.min_length.get()
        max_length = self.max_length.get()
        essential = self.essential_var.get()
        num_comments = self.num_comments.get()
        dir_path = self.dir_path.get()
        file_Name = self.fileName_var.get()

        today = datetime.date.today()
        
        if not (min_length):
            min_length = "0"
        
        if not (max_length):
            max_length = "10"
        
        if not (num_comments):
            num_comments = "10"

        if not essential:
            essential = "台北+餐廳"
        else:
            essential += "餐廳"

        if not file_Name:
            file_Name = "data" + str(today.year) + str(today.month) + str(today.day) + ".txt"
        else:
            file_Name += ".txt"
        
        if not (dir_path):
            messagebox.showerror("錯誤", "請填寫儲存位置")
            return
        
        try:
            min_length = int(min_length)
            max_length = int(max_length)
            num_comments = int(num_comments)
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
            return
        
        if min_length < 0 or max_length <= 0 or num_comments < 10 or num_comments > 10000:
            messagebox.showerror("錯誤", "請輸入有效的數字範圍")
            return
        
        result = f"""
        評論最少字數: {min_length}
        評論最多字數: {max_length}
        關鍵字: {essential}
        需要多少條評論: {num_comments}
        目錄: {dir_path}
        檔案格式: {file_Name}
        """
        messagebox.showinfo("提交結果", result)

        getComment = GC(num_comments, min_length, max_length, essential)
        getComment.main()

        self.save_text_to_file(str(getComment.getResult()) , dir_path, file_Name)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommentCollectSystem(root)
    root.mainloop()
    
