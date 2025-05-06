# select_file.py
# 選擇資料夾、選擇檔案（支援 fallback 選擇）

from InquirerPy import inquirer
import os
from config_handler import load_config, save_config

available_types = load_config()["available_types"]

def list_dirs(base_path):
    dirs = []
    for root, dirnames, _ in os.walk(base_path):
        for dirname in dirnames:
            dirs.append(os.path.join(root, dirname))
    return dirs

def list_files_by_extension(directory, extension):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files

def select_directory(base_path="~"):
    base_dir = os.path.expanduser(base_path)
    dirs = list_dirs(base_dir)
    if not dirs:
        print("❌ 找不到任何資料夾")
        return None
    dir_choice = inquirer.fuzzy(
        message="📂 選擇一個資料夾：",
        choices=dirs,
    ).execute()
    return dir_choice

def select_file_type():
    file_type_choice = inquirer.select(
        message="🗂️ 選擇要搜尋的檔案類型：",
        choices=available_types,
        default=available_types[0],
    ).execute()
    return file_type_choice

def select_file_with_fallback():
    while True:
        directory = select_directory()
        if not directory:
            print("❌ 沒有選擇資料夾，退出。")
            return None

        while True:
            file_type = select_file_type()
            files = list_files_by_extension(directory, file_type)

            if files:
                file_choice = inquirer.fuzzy(
                    message=f"🔍 選擇一個 {file_type} 檔案：",
                    choices=files,
                ).execute()
                return file_choice
            else:
                # 找不到任何該類型檔案，提供 fallback 選單
                fallback_action = inquirer.select(
                    message=f"⚠️ 在 {directory} 找不到任何 {file_type} 檔案，想要？",
                    choices=[
                        "換一個檔案類型",
                        "重新選擇資料夾",
                        "退出"
                    ],
                ).execute()

                if fallback_action == "換一個檔案類型":
                    continue  # 再跳回去選 file type
                elif fallback_action == "重新選擇資料夾":
                    break  # 跳出內層 while，重新選資料夾
                else:
                    print("👋 已退出。")
                    return None
                
                
# file_operation.py

def save_as_new_file(df, original_file_extension, save_csv_func):
    """另存新檔案，支援選擇目錄 + 副檔名 + 存在檢查"""
    while True:
        new_name = input("請輸入新檔案名稱（不要副檔名，只輸入名字）：").strip()

        if not new_name:
            print("⚠️ 必須輸入新檔案名稱。")
            continue

        # 選副檔名
        ext_choice = inquirer.select(
            message="🗂️ 選擇新檔案的副檔名：",
            choices=["使用原本的副檔名"]+available_types,
            default="使用原本的副檔名",
        ).execute()

        if ext_choice == "使用原本的副檔名":
            extension = original_file_extension
        else:
            extension = ext_choice

        if not extension.startswith("."):
            extension = "." + extension

        # 讓使用者選目錄
        print("\n🗂️ 請選擇要儲存到的資料夾：")
        save_dir = select_directory()
        if not save_dir:
            print("⚠️ 沒有選擇儲存目錄，取消另存。")
            return

        full_path = os.path.join(save_dir, new_name + extension)

        # 檢查檔案是否存在
        if os.path.exists(full_path):
            overwrite = inquirer.select(
                message=f"⚠️ 檔案 {full_path} 已存在，怎麼做？",
                choices=["覆蓋", "重新輸入名字", "放棄儲存"],
            ).execute()

            if overwrite == "覆蓋":
                save_csv_func(df, full_path)
                print(f"✅ 已覆蓋並儲存成：{full_path}")
                return
            elif overwrite == "重新輸入名字":
                continue
            else:
                print("⚠️ 選擇放棄儲存，退出。")
                return
        else:
            save_csv_func(df, full_path)
            print(f"✅ 成功另存為新檔案：{full_path}")
            return
