import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob
import pandas as pd
import openpyxl

prefix_url = "https://nakamura196.github.io/sat_iiif"
# prefix_url = "https://sat-iiif.s3.amazonaws.com"
prefix_path = "../docs"

files = glob.glob(prefix_path + "/files/tile/**/*.tif", recursive=True)
files = sorted(files)

ids = []

rows_0 = [
    ["ID", "Title", "Thumbnail", "manifest", "viewingDirection", "Relation", "viewingHint", "rights", "attribution"],
    ["http://purl.org/dc/terms/identifier", "http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://schema.org/url", "http://iiif.io/api/presentation/2#viewingDirection", "http://purl.org/dc/terms/relation", "http://iiif.io/api/presentation/2#viewingHint", "http://purl.org/dc/terms/rights", ""],
    ["Literal", "Literal", "Resource", "Resource", "Resource", "Resource", "Resource", "Resource", "Literal"],
    ["", "", "", "", "", "", ""],
]

rows_1 = [
    ["ID", "Thumbnail"]
]

rows_2 = [
    ["ID", "Original", "Thumbnail", "Width", "Height"]
]

rows_3 = [
    ["label", "url"],
    ["kandomokuroku", prefix_url+"/iiif/collection/kandomokuroku.json"]
]

for i in range(len(files)):
    print(i, len(files), files[i])

    file = files[i]

    try:
        img = Image.open(file)
    except Exception as e:
        print(e)
        continue

    page = file.split("p.")[1].split(".")[0]

    original_url = "https://05r4t6462c.execute-api.us-east-1.amazonaws.com/latest/iiif/2/sat%2Ffiles%2Ftile%2FkandomokurokuJPEG%2Fkandomokuroku%20p."+page+"/info.json"

    thumbnail_url = original_url.replace("info.json", "full/256,/0/default.jpg")  

    id = "kandomokuroku"

    if id not in ids:
        ids.append(id)

        manifest = prefix_url+"/iiif/"+id+"/manifest.json"

        rows_0.append([id, "勘同目録", thumbnail_url, manifest, "http://iiif.io/api/presentation/2#rightToLeftDirection", "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest, "", "http://example.org", "酉蓮社"])

    # rows_1.append([id, thumbnail_url])

    rows_2.append([id, original_url, thumbnail_url, img.width, img.height])

    print(id)

df_0 = pd.DataFrame(rows_0)
df_1 = pd.DataFrame(rows_1)

with pd.ExcelWriter('tmp/main.xlsx') as writer:
    df_0.to_excel(writer, sheet_name='item', index=False, header=False)
    df_1.to_excel(writer, sheet_name='thumbnail', index=False, header=False)
    pd.DataFrame(rows_2).to_excel(writer, sheet_name='media', index=False, header=False)
    pd.DataFrame(rows_3).to_excel(writer, sheet_name='collection', index=False, header=False)
    pd.DataFrame([]).to_excel(writer, sheet_name='toc', index=False, header=False)



