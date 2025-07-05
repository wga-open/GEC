import sys
from cx_Freeze import setup, Executable

# GUI应用程序需要不同的base
base = "Win32GUI" if sys.platform == "win32" else None

# 构建选项
build_options = {
    "packages": ["os", "sys", "json","tkinter","jieba","pandas","logging","PIL","requests",
                 "re","time","threading"],
    "include_files": ["TU/","ui_manager.py","tooltip.py","pagination.py",
                      "lexicon_manager.py","image_loader.py","deepseek_module.py","data_processor.py",
                      "Baidu_Text_transAPI.py","KU.csv","wt.xlsx","logs/"],
    "optimize": 2
}

# 可执行文件配置
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="MyApp",
        copyright="Copyright (C) 2023 My Company",
        shortcut_name="My Application",
        shortcut_dir="DesktopFolder"
    )
]

setup(
    name="WGA",
    version="1.0",
    description="World-Graphic-Alphabet-WGA",
    options={"build_exe": build_options},
    executables=executables
)