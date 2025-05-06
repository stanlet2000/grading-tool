from file_operation import select_file_with_fallback, save_as_new_file
from backend import load_csv, find_student, update_grade, save_csv, is_empty_grade, search_student
import sys
import os

def main():
    file = select_file_with_fallback()
    if not file:
        print("❌ 沒有選擇檔案，退出。")
        sys.exit(1)

    df = load_csv(file)
    print(f"\n=== 成績登記系統 ===\n載入檔案：{file}\n")

    modified = False

    while True:
        student_keyword = input("請輸入學號（或 exit 離開）：").strip()
        if student_keyword.lower() == 'exit':
            break


        result = search_student(df, student_keyword)

        if result is None:
            continue

        student_id = result[0]
        name = result[1]
        grade = result[2]

        print(f"學號：{student_id}")
        print(f"姓名：{name}")
        print(f"目前成績：{'未登記' if is_empty_grade(grade) else grade}")

        try:
            new_grade = input("請輸入新成績：").strip()
            if not new_grade.isdigit() or not (0 <= int(new_grade) <= 100):
                print("❌ 成績請輸入 0 到 100 的整數。\n")
                continue
            df = update_grade(df, student_id, int(new_grade))
            modified = True
            print("✅ 成績暫存完成（尚未儲存）\n")
        except Exception as e:
            print("❌ 錯誤：", e)

    if modified:
        print("\n📋 偵測到有成績修改，請選擇儲存方式：")
        print("1. 儲存到原檔案")
        print("2. 另存新檔案")
        print("3. 不儲存，直接退出")
        choice = input("請輸入選項 (1/2/3)：").strip()

        if choice == "1":
            save_csv(df, file)
            print("✅ 已儲存到原始檔案。")

        elif choice == "2":
            _, original_extension = os.path.splitext(file)
            save_as_new_file(df, original_extension, save_csv)

        else:
            print("⚠️ 所有修改已捨棄。")
    else:
        print("👋 沒有做任何更動，直接結束。")

if __name__ == "__main__":
    main()
