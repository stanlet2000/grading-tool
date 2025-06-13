import pandas as pd
from InquirerPy import inquirer
from config_handler import load_config

config = load_config()
col_elements = config["columns_mapping"]

def load_csv(path):
    delimiter = load_config()["load_delimiter"]
    return pd.read_csv(path, delimiter=delimiter, encoding="utf-8")

def find_student(df, student_id):
    return df[df[col_elements["studentid"]] == student_id]

def update_grade(df, student_id, new_grade):
    df.loc[df[col_elements["studentid"]] == student_id, col_elements["grade"]] = new_grade
    return df

def save_csv(df, path):
    delimiter = load_config()["save_delimiter"]
    df.to_csv(path, index=False, sep=delimiter, encoding="utf-8")

def is_empty_grade(grade):
    return pd.isna(grade)


def search_student(df, keyword):
    """根據關鍵字搜尋學生"""
    keyword_lower = keyword.lower()

    matches = df[df[col_elements["studentid"]].str.lower().str.contains(keyword_lower, na=False)]

    if matches.empty:
        print("❌ 找不到符合的學號。")
        return None

    if len(matches) == 1:
        student = matches.iloc[0]
        print(f"找到符合的學生：{student[col_elements['studentid']]} - {student[col_elements['name']]}")
        return (student[col_elements["studentid"]], student[col_elements["name"]], student[col_elements["grade"]])

    else:
        choices = [
            f"{row[col_elements["studentid"]]} - {row[col_elements["name"]]}"
            for _, row in matches.iterrows()
        ]
        choices.append("🔙 重新輸入學號")

        selected = inquirer.select(
            message="🔍 找到多個符合的學生，請選擇：",
            choices=choices,
        ).execute()

        if selected == "🔙 重新輸入學號":
            return None

        selected_id = selected.split(" - ")[0]
        student = matches[matches[col_elements["studentid"]] == selected_id].iloc[0]
        return (student[col_elements["studentid"]], student[col_elements["name"]], student[col_elements["grade"]])

def check_required_columns(df):
    """檢查 CSV 是否包含所有 mapping 裡定義的外部欄位"""
    config = load_config()
    columns_mapping = config["columns_mapping"]
    df_columns = [col.strip() for col in df.columns]

    missing = []
    for external_col in columns_mapping.values():
        if external_col not in df_columns:
            missing.append(external_col)

    if missing:
        print(f"❌ 檔案缺少必要欄位：{', '.join(missing)}")
        return False
    return True


def drop_unused_columns(df):
    current_columns = df.columns.tolist()

    selected = inquirer.checkbox(
        message="🧹 請選擇要保留的欄位：",
        choices=current_columns,
        instruction="空白鍵選取、上下移動、Enter 確認"
    ).execute()

    if not selected:
        print("⚠️ 你沒有選任何欄位，將保留全部欄位。")
        return df

    columns_to_drop = [col for col in current_columns if col not in selected]

    if columns_to_drop:
        print(f"🧹 將刪除以下欄位：{', '.join(columns_to_drop)}")
        df = df.drop(columns=columns_to_drop)
    else:
        print("✅ 所有欄位都保留。")

    return df
