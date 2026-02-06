import streamlit as st
import pandas as pd
import os
import re

DATA_FILE = "data.csv"

st.set_page_config(page_title="Web Excel", layout="wide")
st.title("Web Excel (with Formulas)")

# =========================
# Data Handling
# =========================
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame({
            "A": ["", "", ""],
            "B": ["", "", ""],
            "C": ["", "", ""]
        })

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# =========================
# Spreadsheet Functions
# (each function separate)
# =========================
def func_SUM(*args):
    return sum(args)

def func_AVERAGE(*args):
    return sum(args) / len(args) if args else 0

def func_MIN(*args):
    return min(args)

def func_MAX(*args):
    return max(args)

def func_ROUND(value, digits=0):
    return round(value, int(digits))

def func_IF(condition, true_val, false_val):
    return true_val if condition else false_val

def func_AND(*args):
    return all(args)

def func_OR(*args):
    return any(args)

def func_NOT(value):
    return not value

def func_LEN(text):
    return len(str(text))

def func_CONCAT(*args):
    return "".join(str(a) for a in args)

# Dictionary of functions
FUNCTIONS = {
    "SUM": func_SUM,
    "AVERAGE": func_AVERAGE,
    "MIN": func_MIN,
    "MAX": func_MAX,
    "ROUND": func_ROUND,
    "IF": func_IF,
    "AND": func_AND,
    "OR": func_OR,
    "NOT": func_NOT,
    "LEN": func_LEN,
    "CONCAT": func_CONCAT,
}

# =========================
# Formula Engine
# =========================
def replace_cell_references(formula, df):
    def replace_cell(match):
        col = match.group(1)
        row = int(match.group(2)) - 1
        try:
            cell_value = df.loc[row, col]
            num = float(cell_value)
            if num.is_integer():
                return str(int(num))
            return str(num)
        except:
            return "0"

    return re.sub(r"([A-Z])(\d+)", replace_cell, formula)


def format_result(value):
    """Convert float like 8.0 into 8"""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def evaluate_formula(value, df):
    if not isinstance(value, str):
        return value

    if not value.startswith("="):
        return value

    formula = value[1:]

    # Replace cell references
    formula = replace_cell_references(formula, df)

    # Replace function names
    for name in FUNCTIONS:
        formula = re.sub(rf"\b{name}\b", f"FUNCTIONS['{name}']", formula)

    try:
        result = eval(formula, {"FUNCTIONS": FUNCTIONS})
        return format_result(result)
    except:
        return "ERR"


def calculate_dataframe(input_df):
    result_df = input_df.copy()

    for col in result_df.columns:
        for i in range(len(result_df)):
            result_df.loc[i, col] = evaluate_formula(
                input_df.loc[i, col],
                input_df
            )
    return result_df

# =========================
# Streamlit UI
# =========================
df = load_data()

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor"
)

result_df = calculate_dataframe(edited_df)

st.subheader("Calculated Result")
st.dataframe(result_df, use_container_width=True)

# =========================
# Save and Export
# =========================
if st.button("Save"):
    save_data(edited_df)
    st.success("Saved!")

excel_file = "export.xlsx"
result_df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        "Download Excel",
        f,
        file_name="spreadsheet.xlsx"
    )
