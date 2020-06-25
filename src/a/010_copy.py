import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob
import shutil

files = glob.glob("/Users/nakamurasatoshi/OneDrive/酉蓮社画像201905-/**/*.jpg",recursive=True )

files = sorted(files)

for i in range(len(files)):
    file = files[i]

    if i % 1000 == 0:
        print(i+1, files, file)
    
    # print(file)
    ofile = file.replace("/Users/nakamurasatoshi/OneDrive/酉蓮社画像201905-/", "../../docs/files/original/")

    dirname = os.path.dirname(ofile)

    os.makedirs(dirname, exist_ok=True)

    if not os.path.exists(ofile):
        try:
            shutil.copyfile(file, ofile)
        except Exception as e:
            print(e)