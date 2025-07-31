import pandas as pd
import os

def load_lexicon(csv_path='KU.csv'):
    """
    加载 KU.csv 词库，返回 dict: {词: [entry, ...]}
    entry: {
        'word': 词,
        'pos': 词性,
        'img_names': [图片名, ...],
        'explain': 释义,
        ...  # 其它字段
    }
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"未找到词库文件: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8', low_memory=False)
    df.columns = df.columns.str.strip()
    lexicon = {}
    for _, row in df.iterrows():
        word = str(row.get('词', '')).strip()
        if not word:
            continue
        img_names = str(row.get('图', '')).split(',') if '图' in row else []
        img_names = [img.strip() for img in img_names if img.strip()]
        entry = {
            'word': word,
            'pos': str(row.get('词性', '')).strip(),
            'img_names': img_names,
            'explain': str(row.get('explain', '')).strip(),
            'id': str(row.get('ID', '')).strip(),
            'num': row.get('NUM', ''),
            # 可扩展其它字段
        }
        lexicon.setdefault(word, []).append(entry)
    return lexicon

def lookup(word, lexicon):
    """
    查找单个字/词，返回 entry 列表（可能为空）
    """
    return lexicon.get(word, [])

# 示例用法
if __name__ == '__main__':
    lexicon = load_lexicon()
    print(lookup('体', lexicon)) 