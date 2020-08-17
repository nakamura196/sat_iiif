import glob
import shutil
import os

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('input_dir', help='/Users/nakamurasatoshi/OneDrive/酉蓮社画像201905-')    # 必須の引数を追加
parser.add_argument('output_dir', help='../../docs/files/original')

args = parser.parse_args()    # 4. 引数を解析

inputDir = args.input_dir
outputDir = args.output_dir

files = glob.glob(inputDir+"/**/*.jpg",recursive=True )

print(files)

files = sorted(files)

for i in range(len(files)):
    file = files[i]

    if i % 1000 == 0:
        print(i+1, files, file)
    
    # print(file)
    ofile = file.replace(inputDir, outputDir)

    dirname = os.path.dirname(ofile)

    os.makedirs(dirname, exist_ok=True)

    if not os.path.exists(ofile):
        try:
            shutil.copyfile(file, ofile)
        except Exception as e:
            print(e)