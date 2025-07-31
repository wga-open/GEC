import tkinter as tk
from tkinter import ttk


class UIManager:
    LANGUAGES = {
        "zh": {
            "input_label": "输入文本（1000字以内）",
            "prev_page": "◀ 上一页",
            "next_page": "▶ 下一页",
            "exit": "✖结束",
            "percent": "{}%",
            "start": "开始解析",
            "info_title": "提示",
            "processing": "处理正在进行中，请稍候...",
            "input_error": "输入错误",
            "input_empty": "请输入有效文本",
            "data_error": "数据处理异常",
            "startup_error": "处理启动失败"
        },
        "en": {
            "input_label": "Enter text (max 1000 chars)",
            "prev_page": "◀ Prev",
            "next_page": "▶ Next",
            "exit": "✖ Exit",
            "percent": "{}%",
            "start": "Start Processing",
            "info_title": "Info",
            "processing": "Processing is in progress, please wait...",
            "input_error": "Input Error",
            "input_empty": "Please enter valid text.",
            "data_error": "Data Processing Error",
            "startup_error": "Failed to start processing"
        },
        "jp": {
            "input_label": "テキストを入力してください（最大1000文字まで）",
            "prev_page": "◀ 前のページ",
            "next_page": "▶ 次のページ",
            "exit": "✖ 終了",
            "percent": "{}%",
            "start": "解析を開始",
            "info_title": "情報",
            "processing": "処理中です。しばらくお待ちください...",
            "input_error": "入力エラー",
            "input_empty": "有効なテキストを入力してください",
            "data_error": "データ処理エラー",
            "startup_error": "処理の開始に失敗しました"
        },
        "ara": {
            "input_label": "أدخل النص (بحد أقصى 1000 حرف)",
            "prev_page": "◀ السابق",
            "next_page": "▶ التالي",
            "exit": "✖ خروج",
            "percent": "{}%",
            "start": "ابدأ المعالجة",
            "info_title": "معلومة",
            "processing": "المعالجة جارية، يرجى الانتظار...",
            "input_error": "خطأ في الإدخال",
            "input_empty": "يرجى إدخال نص صالح",
            "data_error": "خطأ في معالجة البيانات",
            "startup_error": "فشل في بدء المعالجة"
        },
        "fr": {
            "input_label": "Entrez le texte (max 1000 caractères)",
            "prev_page": "◀ Précédent",
            "next_page": "▶ Suivant",
            "exit": "✖ Quitter",
            "percent": "{}%",
            "start": "Commencer le traitement",
            "info_title": "Info",
            "processing": "Traitement en cours, veuillez patienter...",
            "input_error": "Erreur d'entrée",
            "input_empty": "Veuillez entrer un texte valide",
            "data_error": "Erreur de traitement des données",
            "startup_error": "Échec du démarrage du traitement"
        },
        "de": {
            "input_label": "Text eingeben (max. 1000 Zeichen)",
            "prev_page": "◀ Zurück",
            "next_page": "▶ Weiter",
            "exit": "✖ Beenden",
            "percent": "{}%",
            "start": "Verarbeitung starten",
            "info_title": "Info",
            "processing": "Verarbeitung läuft, bitte warten...",
            "input_error": "Eingabefehler",
            "input_empty": "Bitte gültigen Text eingeben",
            "data_error": "Datenverarbeitungsfehler",
            "startup_error": "Start der Verarbeitung fehlgeschlagen"
        },
        "pt": {
            "input_label": "Digite o texto (máx. 1000 caracteres)",
            "prev_page": "◀ Anterior",
            "next_page": "▶ Próximo",
            "exit": "✖ Sair",
            "percent": "{}%",
            "start": "Iniciar Processamento",
            "info_title": "Informação",
            "processing": "Processamento em andamento, aguarde...",
            "input_error": "Erro de entrada",
            "input_empty": "Por favor, insira um texto válido",
            "data_error": "Erro no processamento de dados",
            "startup_error": "Falha ao iniciar o processamento"
        },
        "spa": {
            "input_label": "Ingrese el texto (máximo 1000 caracteres)",
            "prev_page": "◀ Anterior",
            "next_page": "▶ Siguiente",
            "exit": "✖ Salir",
            "percent": "{}%",
            "start": "Iniciar procesamiento",
            "info_title": "Información",
            "processing": "Procesando, por favor espere...",
            "input_error": "Error de entrada",
            "input_empty": "Por favor, ingrese un texto válido.",
            "data_error": "Error en el procesamiento de datos",
            "startup_error": "Error al iniciar el procesamiento"
        },
        "ru": {
            "input_label": "Введите текст (макс. 1000 символов)",
            "prev_page": "◀ Предыдущая",
            "next_page": "▶ Следующая",
            "exit": "✖ Выход",
            "percent": "{}%",
            "start": "Начать обработку",
            "info_title": "Информация",
            "processing": "Обработка выполняется, пожалуйста, подождите...",
            "input_error": "Ошибка ввода",
            "input_empty": "Пожалуйста, введите допустимый текст",
            "data_error": "Ошибка обработки данных",
            "startup_error": "Не удалось запустить обработку"
        }
    }

    current_lang = "zh"

    @classmethod
    def switch_language(cls, lang_code):
        if lang_code in cls.LANGUAGES:
            cls.current_lang = lang_code

    @staticmethod
    def create_base_window(title, geometry="1200x700"):
        root = tk.Tk()
        root.title(title)
        root.geometry(geometry)
        root.minsize(1000, 600)
        return root

    @staticmethod
    def _change_language(lang_code, parent, font_spec, on_start_callback):
        if lang_code in UIManager.LANGUAGES:
            UIManager.current_lang = lang_code

            for widget in parent.winfo_children():
                widget.destroy()

            UIManager.create_input_ui(parent, font_spec, on_start_callback)

    @staticmethod
    def create_input_ui(parent, font_spec, on_start_callback):
        lang = UIManager.LANGUAGES[UIManager.current_lang]

        main_frame = ttk.Frame(parent)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        UIManager.main_frame = main_frame  # 保存引用用于语言切换

        # 顶部语言切换下拉菜单
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(anchor='ne', pady=(0, 10))

        lang_combobox = ttk.Combobox(
            lang_frame,
            values=list(UIManager.LANGUAGES.keys()),
            state="readonly",
            width=10
        )
        lang_combobox.set(UIManager.current_lang.upper())  # 设置默认语言
        lang_combobox.bind("<<ComboboxSelected>>", lambda event: UIManager._change_language(lang_combobox.get().lower(), parent, font_spec, on_start_callback))
        lang_combobox.pack(side=tk.LEFT)

        # 输入说明
        label = ttk.Label(main_frame, text=lang["input_label"], font=font_spec)
        label.pack(pady=10)

        # 文本输入框
        text_input = tk.Text(main_frame, height=12, width=90, font=font_spec, undo=True, autoseparators=True,
                             maxundo=-1)
        text_input.pack(pady=10)

        # 右键菜单
        right_click_menu = tk.Menu(text_input, tearoff=0)
        right_click_menu.add_command(label="Paste", command=lambda: text_input.event_generate("<<Paste>>"))
        right_click_menu.add_command(label="Copy", command=lambda: text_input.event_generate("<<Copy>>"))
        right_click_menu.add_command(label="Cut", command=lambda: text_input.event_generate("<<Cut>>"))

        def show_context_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        text_input.bind("<Button-3>", show_context_menu)

        # 开始按钮
        ttk.Button(
            main_frame,
            text=lang.get("start", "开始解析"),
            command=lambda: on_start_callback(text_input.get("1.0", tk.END)),
            style='TButton'
        ).pack(pady=15, ipadx=20, ipady=8)

        return main_frame, text_input

    @staticmethod
    def create_control_buttons(parent, ratios, ratio_index, on_ratio, on_page, on_exit):
        lang = UIManager.LANGUAGES[UIManager.current_lang]
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=5, padx=10)

        ttk.Button(btn_frame, text=lang["prev_page"], command=lambda: on_page(-1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=lang["next_page"], command=lambda: on_page(1)).pack(side=tk.LEFT, padx=5)

        mode_frame = ttk.Frame(btn_frame)
        mode_frame.pack(side=tk.LEFT, padx=20)
        for ratio in ratios:
            ttk.Button(
                mode_frame,
                text=lang["percent"].format(int(ratio * 100)),
                command=lambda r=ratio: [on_ratio(r), on_page(0)]
            ).pack(side=tk.LEFT, padx=2)

        ttk.Button(btn_frame, text=lang["exit"], command=on_exit).pack(side=tk.RIGHT, padx=10)

        return btn_frame
