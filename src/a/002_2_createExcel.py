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

import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import urllib.parse

# prefix_url = "https://nakamura196.github.io/sat_iiif"
# prefix_url = "https://sat-iiif.s3.amazonaws.com"
prefix_url = "https://d1av1vcgsldque.cloudfront.net"
prefix_path = "../../docs"

ids = []

rows_0 = [
    ["ID", "Title", "Thumbnail", "manifest", "viewingDirection", "Relation", "viewingHint", "rights", "attribution", "大正蔵経典番号", "酉蓮社本経典番号"],
    ["http://purl.org/dc/terms/identifier", "http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://schema.org/url", "http://iiif.io/api/presentation/2#viewingDirection", "http://purl.org/dc/terms/relation", "http://iiif.io/api/presentation/2#viewingHint", "http://purl.org/dc/terms/rights", "", "", ""],
    ["Literal", "Literal", "Resource", "Resource", "Resource", "Resource", "Resource", "Resource", "Literal", "", ""],
    ["", "", "", "", "", "", "", "", "", "metadata", "metadata"],
]

rows_1 = [
    ["ID", "Thumbnail"]
]

rows_2 = [
    ["ID", "Original", "Thumbnail", "Width", "Height"]
]

rows_3 = [
    ["label", "url"],
    ["酉蓮社画像", prefix_url+"/iiif/collection/酉蓮社画像.json"]
]

#----------

path = "data/images.xlsx"

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)



for j in range(1, r_count):

    id = str(df.iloc[j,0])
    print(id)
    label = df.iloc[j,3]

    if not pd.isnull(df.iloc[j,4]):

        manifest = prefix_url+"/iiif/"+id+"/manifest.json"

        dir = "../../docs/files/original/"+df.iloc[j,4]

        start = int(df.iloc[j,5])
        end = int(df.iloc[j,6])

        for i in range(start, end + 1):
            file = dir + "/image"+str(i).zfill(3)+".jpg"
            if os.path.exists(file):
                print(file)

                img = Image.open(file)

                original_url = file.replace(prefix_path, prefix_url)

                thumbnail_path = file.replace("/original/", "/medium/")
                thumbnail_url = thumbnail_path.replace(prefix_path, prefix_url)

                rows_1.append([id, thumbnail_url])

                if id not in ids:

                    rows_0.append([id, label, thumbnail_url, manifest, "http://iiif.io/api/presentation/2#rightToLeftDirection", "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest, "", "http://example.org", "酉蓮社", df.iloc[j, 1], df.iloc[j, 2]])

                    ids.append(id)

                rows_2.append([id, original_url, thumbnail_url, img.width, img.height])

                print(id)

        print("--------")

'''

prefix_url = "https://nakamura196.github.io/sat_iiif"
prefix_path = "../../docs"

files = glob.glob(prefix_path + "/files/original/*/*.jpg", recursive=True)
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
    ["酉蓮社画像", prefix_url+"/iiif/collection/酉蓮社画像.json"]
]

for i in range(len(files)):
    print(i, len(files), files[i])

    file = files[i]

    img = Image.open(file)

    original_url = file.replace(prefix_path, prefix_url)

    thumbnail_path = file.replace("/original/", "/medium/")
    thumbnail_url = thumbnail_path.replace(prefix_path, prefix_url)

    

    id = file.split("/")[-2]

    if id not in ids:
        ids.append(id)

        manifest = prefix_url+"/iiif/"+id+"/manifest.json"

        rows_0.append([id, id, thumbnail_url, manifest, "http://iiif.io/api/presentation/2#rightToLeftDirection", "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest, "", "http://example.org", "酉蓮社"])

    rows_1.append([id, thumbnail_url])

    rows_2.append([id, original_url, thumbnail_url, img.width, img.height])

    print(id)

'''

df_0 = pd.DataFrame(rows_0)
df_1 = pd.DataFrame(rows_1)

with pd.ExcelWriter('data/main3.xlsx') as writer:
    df_0.to_excel(writer, sheet_name='item', index=False, header=False)
    df_1.to_excel(writer, sheet_name='thumbnail', index=False, header=False)
    pd.DataFrame(rows_2).to_excel(writer, sheet_name='media', index=False, header=False)
    pd.DataFrame(rows_3).to_excel(writer, sheet_name='collection', index=False, header=False)
    pd.DataFrame([]).to_excel(writer, sheet_name='toc', index=False, header=False)


