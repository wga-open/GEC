# data_processor.py
import logging
import re
from collections import defaultdict
from typing import List, Dict, Optional, Any
import jieba

class DataProcessor:
    @staticmethod
    def extract_chinese_word(annotation: str) -> str:
        """
        智能提取中文词核心逻辑（兼容多种注解格式）

        参数：
            annotation: 原始注解字符串，如 "apple~苹果" 或 "纽约~New York"

        返回：
            纯中文词，如 "苹果" 或 "纽约"
        """
        try:
            if not isinstance(annotation, str):
                return ""

            # 处理多段式注解（优先取最后一个有效段）
            # segments = [s.strip() for s in annotation.split('~') if s.strip()]
            # if not segments:
            #     return ""
            #
            # # 取最后一个段作为主要处理内容
            # processing_text = segments[-1]
            #
            # # 过滤非中文字符（至少保留第一个字符）
            # chinese_chars = [c for c in processing_text if '\u4e00' <= c <= '\u9fff']
            # if not chinese_chars:
            #     return processing_text[:1] if processing_text else ""
            # return ''.join(chinese_chars)
            return ''.join(re.findall(r'[\u4e00-\u9fff]', annotation))

        except Exception as e:
            logging.error(f"中文词提取异常 | 输入：{annotation} | 错误：{str(e)}")
            return ""

    @staticmethod
    def find_best_match(annotation: str,pos, lexicon: Dict) -> Optional[Dict]:
        """
        多级词库匹配算法（支持词性标记）

        参数：
            annotation: 需要匹配的注解词
            lexicon: 加载的词库字典

        返回：
            匹配到的最佳词条，或None
        """
        try:
            if not lexicon:
                return None
            # 如果是标点符号和数字，直接匹配
            if pos == 'spec':
                base = annotation  # 去掉 'spec'
                # 1. 如果整串能直接匹配就直接返回
                if base in lexicon:
                    return lexicon[base][0]
                # 2. 否则，如果全是数字，就逐字符拆分再组合
                # if base.isdigit():
                #     result_entries = []
                #     for ch in base:
                #         # 安全检查：只有存在才取
                #         if ch in lexicon:
                #             result_entries.append(lexicon[ch][0])
                #     entry={
                #         'word': base,
                #         "images": [i.get('images')[0] for i in result_entries],
                #         "english_text": base,
                #         "img_names":[i.get('img_names')[0] for i in result_entries]
                #
                #     }
                #     return entry
                if all(ch in lexicon for ch in base):
                    result_entries = [lexicon[ch][0] for ch in base]

                    # 组装返回结构，兼容 keys 不存在的情况
                    images = []
                    img_names = []
                    for entry in result_entries:
                        if 'images' in entry and entry['images']:
                            images.append(entry['images'][0])
                        if 'img_names' in entry and entry['img_names']:
                            img_names.append(entry['img_names'][0])

                    entry = {
                        'word': base,
                        'images': images,
                        'eng_text': base,
                        'img_names': img_names
                    }
                    return entry


            chinese_word = DataProcessor.extract_chinese_word(annotation)
            if not chinese_word:
                return None

            # 提取词性标记（如果有）
            # pos = ''.join(re.findall(r'[a-zA-Z]', annotation))

            # 匹配策略优先级：
            # 1. 完全匹配（包含词性标记）
            if chinese_word in lexicon:
                candidates = lexicon[chinese_word]
                if candidates:
                    # 优先选择词性匹配的词条
                    pos_matches = [c for c in candidates if c['pos'] == pos]
                    if pos_matches:
                        return DataProcessor._select_best_candidate(pos_matches)
                    else:
                        return DataProcessor._select_best_candidate(candidates)

            # 2. 去除词性标记后匹配（如 "跑V" -> "跑"）
            base_word = chinese_word.rstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if base_word and base_word in lexicon:
                candidates = lexicon[base_word]
                if candidates:
                    # 优先选择词性匹配的词条
                    pos_matches = [c for c in candidates if c['pos'] == pos]
                    if pos_matches:
                        return DataProcessor._select_best_candidate(pos_matches)
                    else:
                        return DataProcessor._select_best_candidate(candidates)

            # 3. 单字匹配（保底策略）
            if len(chinese_word) == 1 and chinese_word in lexicon:
                candidates = lexicon[chinese_word]
                if candidates:
                    # 优先选择词性匹配的词条
                    pos_matches = [c for c in candidates if c['pos'] == pos]
                    if pos_matches:
                        return DataProcessor._select_best_candidate(pos_matches)
                    else:
                        return DataProcessor._select_best_candidate(candidates)

            return None

        except Exception as e:
            logging.error(f"词库匹配异常 | 输入：{annotation} | 错误：{str(e)}")
            return None

    @staticmethod
    def _select_best_candidate(candidates: List[Dict]) -> Dict:
        """按NUM字段选择最优候选词条"""
        return min(candidates, key=lambda x: x.get('num', 9999))

    @staticmethod
    def split_word(word: str, lexicon: Dict) -> List[str]:
        """
        逆向最大匹配分词算法（从右向左拆分）

        参数：
            word: 需要拆分的中文词，如 "中华人民共和国"
            lexicon: 词库字典

        返回：
            拆分后的子词列表，如 ["中华", "人民", "共和国"]
        """
        try:
            if len(word) < 2:
                return [word]
            if word in lexicon:
                return [word]


            #使用jieba进行分词
            sol=jieba.lcut(word)
            j=0
            retsol=[]
            for i in sol:
                if DataProcessor.find_best_match(i,None, lexicon):
                    j+=1
                    if j!=len(sol):
                        retsol+=[i]+['小隔']
                    else:
                        retsol+=[i]
            if j==len(sol):
                return retsol
            # 从右向左寻找最长匹配
            for i in range(len(word)-1, 0, -1):
                right_part = word[i:]
                if DataProcessor.find_best_match(right_part,None, lexicon) :
                    left_part = word[:i]
                    if DataProcessor.find_best_match(left_part,None, lexicon):
                        return [left_part]+['小隔']  + [right_part]
                    # return DataProcessor.split_word(left_part, lexicon) + [right_part]

            for i in range(1, len(word)):
                right_part = word[i:]
                if DataProcessor.find_best_match(right_part,None, lexicon):
                    left_part = word[:i]
                    if DataProcessor.find_best_match(left_part,None, lexicon):
                        return [left_part]+['小隔']  + [right_part]
                    # return DataProcessor.split_word(left_part, lexicon) +['小隔'] + [right_part]

            # 保底处理：单字拆分（过滤无效字符）
            clist = []
            for c in word:
                if '\u4e00' <= c <= '\u9fff':
                    clist.append(c)
                    if not c == word[-1]:
                        clist.append('小隔')

            return clist

        except Exception as e:
            logging.error(f"分词异常 | 输入：{word} | 错误：{str(e)}")
            return [word]

    @staticmethod
    def process_token(annotation: str,pos, lexicon: Dict) -> list[Any] | tuple[list[Any], list[Any]]:
        """
        统一处理入口（带完整日志记录）

        参数：
            annotation: 原始注解字符串
            lexicon: 加载的词库字典

        返回：
            匹配到的图片列表
        """
        try:
            logging.info(f"开始处理词条 | 注解：{annotation}")
            entry = []
            # 直接匹配流程
            direct_match = DataProcessor.find_best_match(annotation,pos, lexicon)
            if direct_match:
                logging.debug(f"直接匹配成功 | 注解：{annotation} → 词条ID：{direct_match.get('id')}")
                return [direct_match]

            # 拆分匹配流程
            chinese_word = DataProcessor.extract_chinese_word(annotation)
            logging.debug(f"进入拆分流程 | 原始词：{chinese_word}")

            split_parts = DataProcessor.split_word(chinese_word, lexicon)
            logging.info(f"拆分结果 | 原始词：{chinese_word} → 子词：{split_parts}")

            images = []

            for part in split_parts:
                sub_entry = DataProcessor.find_best_match(part,pos, lexicon)
                if sub_entry:
                    logging.debug(f"子词匹配成功 | 子词：{part} → 词条ID：{sub_entry.get('id')}")

                    entry.append(sub_entry)
            # merged_dict = defaultdict(list)
            # for sub_dict in entry:
            #     for key, value in sub_dict.items():
            #         merged_dict[key].append(value)
            #
            # # 将 defaultdict 转换为普通字典
            # entry= dict(merged_dict)
            # print(entry)

            return entry

        except Exception as e:
            logging.error(f"处理流程异常 | 输入：{annotation} | 错误：{str(e)}")
            return []

    @staticmethod
    def calculate_width(word: str, images: list, config: dict) -> int:
        """像素级精确计算（严格实现最新需求）"""
        try:
            # 确保 config 中包含 'font'
            if 'font' not in config:
                raise KeyError("config 字典中缺少 'font' 键")

            # 文本基础宽度（严格按font测量）
            base_text_width = config['font'].measure(word)

            # 最终文本宽度 = 基础宽度 + 左右边距*2
            text_width = base_text_width + config['text_padding'] * 2

            # 图片总宽度（严格计算间距）
            img_width = 0
            if images:
                img_width = sum(img.width() for img in images)
                img_width += (len(images) - 1) * config['img_spacing']  # 严格应用图母间距

            # 最终宽度取最大值并确保最小宽度
            final_width = max(text_width, img_width, config['min_width'])

            logging.debug(f"宽度计算 | 文本：{text_width}px | 图片：{img_width}px | 最终：{final_width}px")
            return final_width

        except Exception as e:
            logging.error(f"宽度计算失败: {str(e)}")
            return config['min_width']