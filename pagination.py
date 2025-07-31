import logging
import tkinter as tk
from tkinter import ttk

from Baidu_Text_transAPI import createRequest
from ui_manager import UIManager
from tooltip import Tooltip



class PaginationManager:
    @staticmethod
    def paginate_content(entries, config):
        """分页处理核心逻辑"""
        pages = []
        current_page = []
        current_height = 0
        line_buffer = []
        line_width = 0

        for entry in entries:
            if entry.get('type') == 'paragraph_end':
                if line_buffer:
                    current_page.append({'type': 'line', 'content': line_buffer.copy()})
                    current_height += config['line_height']
                    line_buffer.clear()
                    line_width = 0

                current_page.append({'type': 'paragraph_space'})
                current_height += config['para_space']

                if current_height > config['page_max_height']:
                    pages.append(current_page.copy())
                    current_page.clear()
                    current_height = 0
                continue

            entry_width = entry.get('width', config['min_width'])
            if line_width + entry_width > config['max_line_width']:
                current_page.append({'type': 'line', 'content': line_buffer.copy()})
                current_height += config['line_height']
                line_buffer = [entry]
                line_width = entry_width + config['word_spacing']

                if current_height + config['line_height'] > config['page_max_height']:
                    pages.append(current_page.copy())
                    current_page.clear()
                    current_height = 0
            else:
                line_buffer.append(entry)
                line_width += entry_width + config['word_spacing']

        if line_buffer:
            current_page.append({'type': 'line', 'content': line_buffer})
            current_height += config['line_height']

        if current_page:
            pages.append(current_page)

        return pages

    @staticmethod
    def render_page(app, page_num, pages, config):
        """页面渲染核心逻辑（修复重复文本问题）"""
        app.current_page = max(0, min(page_num, len(pages) - 1))
        app.clear_window()

        # 获取当前显示比例
        current_ratio = config['display_ratios'][config['ratio_index']]

        # 最外层容器
        outer_frame = ttk.Frame(app.root, style='Main.TFrame')
        outer_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 控制按钮
        control_frame = UIManager.create_control_buttons(
            parent=outer_frame,
            ratios=config['display_ratios'],
            ratio_index=config['ratio_index'],
            on_ratio=app._set_display_ratio,
            on_page=app._change_page,
            on_exit=app._show_input_ui
        )
        control_frame.pack(pady=(0, 10), fill='x')

        # 内容区域
        content_frame = ttk.Frame(outer_frame, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True)

        # 滚动画布
        canvas = tk.Canvas(content_frame, bg='white', highlightthickness=0)
        scroll_y = ttk.Scrollbar(content_frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        scroll_y.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        # 内容容器
        container = ttk.Frame(canvas, style='Content.TFrame')
        canvas.create_window((0, 0), window=container, anchor='nw')

        def _update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        container.bind('<Configure>', _update_scrollregion)
        enlist=[]
        imgnamelist=[]
        # if UIManager.current_lang == 'jp':
        #     if pages and pages[app.current_page]:
        #         for item in pages[app.current_page]:
        #             if item['type'] == 'line':
        #                 for idx, entry in enumerate(item['content']):
        #                     enlist.append(entry['china'])
        #                     if entry['images']!=  None:
        #                         imgnamelist.append(entry['images'])
        #
        #     sol=createRequest('\n'.join(enlist), 'zh', 'jp')
        #     time.sleep(1)
        #     # sol_imgname=createRequest('\n'.join(imgnamelist), 'zh', 'jp')
        #
        #     count=0
        #     if pages and pages[app.current_page]:
        #         id=0
        #         for item in pages[app.current_page]:
        #             if item['type'] == 'line':
        #                 for idx, entry in enumerate(item['content']):
        #                     entry['jp']=sol[id]
        #                     id+=1
                            # if entry['images']!=  None:
                            #     entry['image_name_jp']=sol_imgname[idx-count]
                            # else:
                            #     count+=1

        # 渲染内容
        if pages and pages[app.current_page]:
            for item in pages[app.current_page]:
                if item['type'] == 'paragraph_space':
                    spacer = ttk.Frame(container, height=4, style='Line.TFrame')
                    spacer.pack(fill='x')
                    # ttk.Frame(container, height=15).pack(fill='x')
                    continue

                if item['type'] == 'line':
                    line_frame = ttk.Frame(container, style='Line.TFrame')
                    line_frame.pack(fill='x', anchor='nw', expand=True)

                    for idx, entry in enumerate(item['content']):
                        # 计算内容宽度
                        img_width = 0
                        if entry['images']:
                            img_width = sum(img.width() for img in entry['images'])
                            if len(entry['images']) > 1:
                                img_width += (len(entry['images']) - 1) * config['img_spacing']

                        text_width = config['font'].measure(entry['text'])
                        content_width = max(img_width, text_width)

                        # 词条容器
                        word_frame = ttk.Frame(
                            line_frame,
                            width=content_width + 8,
                            height=config['line_height'],
                            style='Word.TFrame'
                        )
                        word_frame.pack_propagate(False)
                        # word_frame.pack()
                        if idx == 0:
                            word_frame.pack(side='left', padx=(0,0))
                        else:
                            word_frame.pack(side='left', padx=(0, 0))

                        # 图片渲染
                        # if entry['images']:
                        img_container = ttk.Frame(
                            word_frame,
                            height=25,
                            style='ImgContainer.TFrame'
                        )
                        img_container.pack_propagate(False)
                        img_container.pack(fill='x', pady=(0, 4))

                        img_canvas = tk.Canvas(
                            img_container,
                            width=content_width + 8,
                            height=25,
                            bg='white',
                            highlightthickness=0,
                            bd=0
                        )
                        img_canvas.pack_propagate(False)
                        img_canvas.pack()

                        x_offset = (content_width + 8 - img_width) // 2
                        x_pos = x_offset
                        if entry['images']!=  None:
                            for img,img_name in zip(entry['images'],entry['img_names']):
                                lbl = ttk.Label(img_canvas, image=img, background='white')
                                lbl.image = img
                                lbl.place(x=x_pos, y=0, anchor='nw')
                                if 'text' in entry:
                                    info_list = app.lexicon.get(img_name, [])
                                    if info_list:
                                        explain = info_list[0].get('explain', [])
                                        if explain=='小隔':
                                            explain=''
                                        en=info_list[0].get('eng_text', '')
                                        jp=info_list[0].get('jp_text', '')
                                        ara=info_list[0].get('ara_text', '')
                                        fr=info_list[0].get('fr_text', '')
                                        de=info_list[0].get('de_text', '')
                                        pt=info_list[0].get('pt_text', '')
                                        spa=info_list[0].get('spa_text', '')
                                        ru=info_list[0].get('ru_text', '')
                                    else:
                                        explain = 'no explain'
                                        en  = 'nan en'
                                        jp =  'nan jp'
                                        ara = 'nan ara'
                                        fr = 'nan fr'
                                        de = 'nan de'
                                        pt = 'nan pt'
                                        spa = 'nan spa'
                                        ru = 'nan ru'


                                    if UIManager.current_lang == 'zh':
                                        Tooltip(lbl, explain+'\n'+en, position='above')
                                    elif UIManager.current_lang == 'en':

                                        Tooltip(lbl, en+'\n'+explain, position='above')
                                    elif UIManager.current_lang == 'jp':

                                        # jp1 = createRequest(explain, 'zh', 'jp')[0]
                                        # time.sleep(0.5)
                                        Tooltip(lbl,jp+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'ara':
                                        Tooltip(lbl, ara+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'fr':
                                        Tooltip(lbl, fr+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'de':
                                        Tooltip(lbl, de+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'pt':
                                        Tooltip(lbl, pt+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'spa':
                                        Tooltip(lbl, spa+'\n'+en, position='above')
                                    elif  UIManager.current_lang == 'ru':
                                        Tooltip(lbl, ru+'\n'+en, position='above')


                                x_pos += img.width() + config['img_spacing']

                        # 文字区域
                        text_frame = ttk.Frame(
                            word_frame,
                            height=14,
                            style='Text.TFrame'
                        )
                        text_frame.pack_propagate(False)
                        text_frame.pack(fill='both', expand=True)

                        def is_all_spaces(val):
                            if isinstance(val, str):  # 判断是否为字符串
                                return val != "" and val.isspace()  # 判断非空且全是空格字符
                            return False  # 不是字符串直接返回 False
                        # 清除之前的部件
                        for widget in text_frame.winfo_children():
                            widget.destroy()
                        try :
                            if entry['english'] =='' or is_all_spaces(entry['english']) or 'nan' in entry['english']:
                                entry['english']= createRequest(entry['text'], 'zh', 'en')[0]
                            if (entry['jp_text'] =='' or is_all_spaces(entry['jp_text']) or 'nan' in entry['jp_text'])  and UIManager.current_lang == 'jp' :
                                entry['jp_text']= createRequest(entry['china'], 'zh', 'jp')[0]
                            if (entry['ara_text'] =='' or is_all_spaces(entry['ara_text']) or 'nan' in entry['ara_text'])  and UIManager.current_lang == 'ara' :
                                entry['ara_text']= createRequest(entry['china'], 'zh', 'ara')[0]
                            if (entry['fr_text'] ==''  or is_all_spaces(entry['fr_text']) or 'nan' in entry['fr_text']) and UIManager.current_lang == 'fr' :
                                entry['fr_text']= createRequest(entry['china'], 'zh', 'fr')[0]
                            if (entry['de_text'] ==''  or is_all_spaces(entry['de_text']) or 'nan' in entry['de_text']) and UIManager.current_lang == 'de' :
                                entry['de_text']= createRequest(entry['china'], 'zh', 'de')[0]
                            if (entry['pt_text'] =='' or is_all_spaces(entry['pt_text']) or 'nan' in entry['pt_text'])  and UIManager.current_lang == 'pt' :
                                entry['pt_text']= createRequest(entry['china'], 'zh', 'pt')[0]
                            if (entry['spa_text'] == '' or is_all_spaces(entry['spa_text']) or 'nan' in entry['spa_text'])  and UIManager.current_lang == 'spa' :
                                entry['spa_text']= createRequest(entry['china'], 'zh', 'spa')[0]
                            if (entry['ru_text'] == '' or is_all_spaces(entry['ru_text']) or 'nan' in entry['ru_text'])  and UIManager.current_lang == 'ru' :
                                entry['ru_text']= createRequest(entry['china'], 'zh', 'ru')[0]
                        except Exception as e:
                            logging.error(e)


                        # 根据比例调整文字显示
                        if current_ratio < 1:
                            visible_height = int((config['line_height'] - 25 - 4) * current_ratio)

                            # 使用Canvas同时显示文本和遮盖层
                            text_canvas = tk.Canvas(
                                text_frame,
                                bg='white',
                                highlightthickness=0,
                                width=content_width + 4,
                                height=14
                            )
                            text_canvas.pack_propagate(False)
                            text_canvas.pack(fill='both', expand=True)
                            if UIManager.current_lang == 'zh':
                                Tooltip(text_canvas, entry['china'] +'\n'+ entry['english'])
                            elif UIManager.current_lang == 'en':
                                Tooltip(text_canvas, entry['english'] +'\n'+ entry['china'])
                            elif UIManager.current_lang == 'jp':
                                Tooltip(text_canvas, entry['jp_text']+'\n' + entry['china'])
                            # 创建文本
                            text_id = text_canvas.create_text(
                                (content_width + 4) // 2,
                                (config['line_height'] - 25 - 4) // 2,
                                text=entry['text'],
                                font=app.custom_font,
                                anchor='center',
                                width=content_width + 4
                            )

                            # 创建遮盖层
                            text_canvas.create_rectangle(
                                0, visible_height,
                                content_width + 4, config['line_height'] - 25 - 4,
                                fill='white', outline='white'
                            )
                        else:
                            # 完整显示文本
                            text_label = ttk.Label(
                                text_frame,
                                text=entry['text'],
                                font=app.custom_font,
                                anchor='n',
                                padding=(4, 0),
                                wraplength=content_width + 4
                            )
                            text_label.pack(fill='both', expand=True)

                            if UIManager.current_lang == 'zh':
                                Tooltip(text_label, entry['china'] +'\n'+ entry['english'])
                            elif UIManager.current_lang == 'en':
                                Tooltip(text_label, entry['english'] +'\n'+ entry['china'])
                            elif UIManager.current_lang == 'jp':
                                # jp = createRequest(entry['china'], 'zh-CHS2', 'ja')
                                Tooltip(text_label,  entry['jp_text']+'\n'+ entry['china'])
                            elif UIManager.current_lang == 'ara':
                                Tooltip(text_label, entry['ara_text'] +'\n'+ entry['china'])
                            elif  UIManager.current_lang == 'fr':
                                Tooltip(text_label, entry['fr_text'] +'\n'+ entry['china'])
                            elif  UIManager.current_lang == 'de':
                                Tooltip(text_label, entry['de_text'] +'\n'+ entry['china'])
                            elif  UIManager.current_lang == 'pt':
                                Tooltip(text_label, entry['pt_text'] +'\n'+ entry['china'])
                            elif  UIManager.current_lang == 'spa':
                                Tooltip(text_label, entry['spa_text'] +'\n'+ entry['china'])
                            elif  UIManager.current_lang == 'ru':
                                Tooltip(text_label, entry['ru_text'] +'\n'+ entry['china'])

                        # 分隔线
                        if idx < len(item['content']) - 1:
                            sep = ttk.Separator(
                                line_frame,
                                orient='vertical',
                                style='VSep.TSeparator'
                            )
                            sep.pack(side='left', fill='y')

                    ttk.Frame(container, height=8).pack(fill='x')

        # 强制更新布局
        container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

        def _on_mousewheel(event):
            # Windows/Linux 滚动
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        canvas.bind_all("<MouseWheel>", _on_mousewheel)



