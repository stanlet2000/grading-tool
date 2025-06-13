# 📘 Grade Entry CLI Tool

A lightweight and interactive command-line tool for recording student grades based on student IDs. Built with Python, it provides a streamlined interface using `InquirerPy` and `pandas` for fast and flexible CSV manipulation — ideal for instructors, TAs, and data handlers working with grading sheets.

---

## 🚀 Features

### 📁 File Selection & Format Validation
- Interactive file selection (supports `.csv`, `.txt`, `.json`, etc.)
- Manual selection of CSV delimiters (`,`, `;`, `\t`, `|`)
- Validates required columns (e.g., `student ID`, `name`, `grade`)
- Column mapping supported (e.g., `studentid → 學號`)

---

### 🧼 Data Cleaning Tools
- ✅ Keep only selected columns (drop others)
- 🚧 Clear all grade fields (coming soon)
- Standardize column names internally for consistent access

---

### ✏️ Grade Entry & Update
- Case-insensitive and partial match search for student ID
- Show and update existing grades
- Safe interactions: support for cancel, undo, and return
- Save prompt only appears when data is modified

---

### 💾 Save & Export
- Detects modification and prompts whether to save
- "Save As" supported (custom filename and extension)
- Configurable output delimiter and format

---

### ⚙️ Configurable Settings (`configure.json`)
- Define accepted file extensions
- Column name mapping (e.g., `grade → 成績`)
- Default CSV delimiter

---

## 🧰 Dependencies

- [`pandas`](https://pandas.pydata.org/)
- [`InquirerPy`](https://github.com/kazhala/InquirerPy)
- Python 3.10+

---

## 📂 Project Structure
```text
grading-tool/
│
├── main.py # CLI entry point
├── backend.py # Grade search and update logic
├── file_operation.py # File I/O: load, save, export
├── config_handler.py # Read/write configuration file
├── configure.json # User-defined settings (column mapping, file types, etc.)
└── README.md # Project documentation
```


---

## 📦 Installation & Usage

### Requirements

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed

---

### 🔧 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/grading-tool.git
cd grading-tool

# Install dependencies
poetry install
```

### 🚀 Run the CLI
```bash
# Activate the virtual environment
eval $(poetry env activate)

# Start the grading tool
python main.py
```
Alternatively, you can run it directly:
```bash
poetry run python main.py
```