import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob

files = glob.glob("../../docs/files/**/*.jpg", recursive=True)

for i in range(len(files)):
    print(i, len(files), files[i])

    file = files[i]
    dirname = os.path.dirname(file)
    odirname = dirname.replace("/original/", "/medium/")

    os.makedirs(odirname, exist_ok=True)

    img = Image.open(file)

    img_resize = img.resize((256,round(img.height * 256 / img.width)))
    img_resize.save(file.replace("/original/", "/medium/"))


'''

books = ["MCJB01249"]

url = "http://www.tbcas.jp/ja/lib/lib1/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
aas = soup.find_all("a")
for a in aas:
    href = a.get("href")

    if "lib5" in href:
        books.append(href.split("/data/")[1])

for i in range(0, len(books)):

    sleep(1)

    print(str(i+1)+"/"+str(len(books)))

    book = books[i]

    loop_flg = True  

    # print(book)

    page = 1

    while loop_flg:

        path  = "tmp/"+book.replace("/", "-")+"_"+str(page).zfill(3)+".json"

        print(str(book)+"_"+str(page))

        if not os.path.exists(path):

           

            text = None

            page_str = str(page).zfill(4)

            try:

                src = "http://www.tbcas.jp/ja/lib/lib5/data/"+book+"/files/assets/flash/pages/page"+page_str+"_l.jpg"
                # print(src)

                image = Image.open(urllib.request.urlopen(src))
                width, height = image.size

                thumb = "http://www.tbcas.jp/ja/lib/lib5/data/"+book+"/files/assets/flash/pages/page"+page_str+"_s.png"
            except:
                src = "http://design-ec.com/d/e_others_50/l_e_others_500.png"
                width = "600"
                height = "600"
                thumb = "http://design-ec.com/d/e_others_50/l_e_others_500.png"

                loop_flg = False
                continue

            obj = {
                "original": src,
                "thumbnail": thumb,
                "book": book,
                "page": page,
                "width": width,
                "height": height
            }

            if text != None and text != "":
                obj["text"] = text.text.strip()

            with open(path, 'w') as outfile:
                json.dump(obj, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        
        page += 1

       
'''