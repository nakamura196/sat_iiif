import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests

prefix = "https://nakamura196.github.io/sat_iiif"
# prefix = "https://sat-iiif.s3.amazonaws.com"
# prefix = "https://d1av1vcgsldque.cloudfront.net"
odir = "../docs"
path = "tmp/main.xlsx"

def get_collection(df):

    label = df.iloc[1, 0]
    url = df.iloc[1, 1]

    return label, url


df_item = pd.read_excel(path, sheet_name="item", header=None, index_col=None)
df_collection = pd.read_excel(path, sheet_name="collection", header=None, index_col=None)

r_count = len(df_item.index)
c_count = len(df_item.columns)

collection_label, collection_url = get_collection(df_collection)

manifests = []

for i in range(0, c_count):
    label = df_item.iloc[0, i]
    uri = df_item.iloc[1, i]
    # type = df.iloc[2, i]
    target=df_item.iloc[3,i]

    if uri == "http://purl.org/dc/terms/title":
        title_index = i

    if label == "manifest":
        manifest_index = i

    if uri == "http://xmlns.com/foaf/0.1/thumbnail":
        thumbnail_index = i
    

for j in range(4, r_count):

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
      "@type": "sc:Manifest",
      "@id": df_item.iloc[j, manifest_index],
      "label": df_item.iloc[j, title_index]
    }

    manifests.append(manifest)

    thumbnail = df_item.iloc[j, thumbnail_index]
    if not pd.isnull(thumbnail) and thumbnail != 0:
        manifest["thumbnail"] = thumbnail
    
    
collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": collection_url,
    "@type": "sc:Collection",
    "label": collection_label,
    "manifests": manifests,
    "vhint": "use-thumb"
}

opath = collection_url.replace(prefix, odir)
tmp = os.path.split(opath)

os.makedirs(tmp[0], exist_ok=True)

f2 = open(opath, 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

