import requests
import sqlite3

url = 'https://vietphrase.info/Vietphrase/TranslateHanViet'
thieu_list = ["劃", "撿", "誒", "噠", "頜", "擼"]

for word in thieu_list:
    myobj = {'chineseContent': word}
    x = requests.post(url, json = myobj)
    y = str(x.text).strip()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO hanviet (tieng_trung, tieng_viet) VALUES (?, ?)", (word, y))
    conn.commit()
    conn.close()