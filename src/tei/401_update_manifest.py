import os
import argparse
import sys
import json

path = "../../docs/iiif/8483/manifest2.json"

json_open = open(path, 'r')
df = json.load(json_open)

canvases = df["sequences"][0]["canvases"]

prefix = "https://d1av1vcgsldque.cloudfront.net/files/original/1564 釋禪波羅蜜次第法門10卷/"
prefix3 = "https://d1av1vcgsldque.cloudfront.net/files/medium/1564 釋禪波羅蜜次第法門10卷/"
prefix2 = "https://05r4t6462c.execute-api.us-east-1.amazonaws.com/latest/iiif/2/sat%2Ffiles%2Ftile%2F1564%2F"

for canvas in canvases:
    print(canvas)
    canvas["thumbnail"]["@id"] = canvas["thumbnail"]["@id"].replace(prefix3, prefix2).replace(".jpg", "/full/200,/0/default.jpg")

    resource = canvas["images"][0]["resource"]
    resource["@id"] = resource["@id"].split("/full")[0]
    resource["service"] = {
                  "@id": resource["@id"].replace(prefix, prefix2).replace(".jpg", ""),
                  "@context": "http://iiif.io/api/image/2/context.json",
                  "profile": "http://iiif.io/api/image/2/level1.json"
                }

fw = open(path.replace("manifest2", "manifest3"), 'w')
json.dump(df, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))