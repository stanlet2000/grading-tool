import pandas as pd
from InquirerPy import inquirer

def load_csv(path):
    return pd.read_csv(path)

def find_student(df, student_id):
    return df[df['學號'] == student_id]

def update_grade(df, student_id, new_grade):
    df.loc[df['學號'] == student_id, '成績'] = new_grade
    return df

def save_csv(df, path):
    df.to_csv(path, index=False)

def is_empty_grade(grade):
    return pd.isna(grade)


def search_student(df, keyword):
    """根據關鍵字搜尋學生"""
    keyword_lower = keyword.lower()

    matches = df[df['學號'].str.lower().str.contains(keyword_lower, na=False)]

    if matches.empty:
        print("❌ 找不到符合的學號。")
        return None

    if len(matches) == 1:
        return matches.iloc[0]

    else:
        choices = [
            f"{row['學號']} - {row['姓名']}"
            for _, row in matches.iterrows()
        ]
        selected = inquirer.select(
            message="🔍 找到多個符合的學生，請選擇：",
            choices=choices,
        ).execute()

        selected_id = selected.split(" - ")[0]
        return matches[matches['學號'] == selected_id].iloc[0]