import os
import random
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt


def show_csv_head(csv_path, n=5):
    print(f"\n读取 {csv_path} 前{n}行:")
    df = pd.read_csv(csv_path, encoding='utf-8', nrows=n)
    print(df)

def show_excel_head(excel_path, n=5):
    print(f"\n读取 {excel_path} 前{n}行:")
    df = pd.read_excel(excel_path, nrows=n)
    print(df)

def show_random_image(img_dirs):
    all_imgs = []
    for d in img_dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    all_imgs.append(os.path.join(root, f))
    if not all_imgs:
        print("未找到图片文件。"); return
    img_path = random.choice(all_imgs)
    print(f"\n随机展示图片: {img_path}")
    img = Image.open(img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def main():
    while True:
        print("\n==== World Graphic Alphabet WGA Demo ====")
        print("1. 展示 KU.csv 前几行")
        print("2. 展示 wt.xlsx 前几行")
        print("3. 随机展示 src/ 或 TU/ 目录下的一张图片")
        print("0. 退出")
        choice = input("请选择功能: ")
        if choice == '1':
            show_csv_head('KU.csv')
        elif choice == '2':
            show_excel_head('wt.xlsx')
        elif choice == '3':
            show_random_image(['src', 'TU'])
        elif choice == '0':
            print("退出 demo."); break
        else:
            print("无效选择，请重试。")

if __name__ == '__main__':
    main() 