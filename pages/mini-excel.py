import re
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path("data.csv")
EXPORT_FILE = Path("export.xlsx")
DEFAULT_COLUMNS = ["A", "B", "C"]


st.set_page_config(page_title="Web Excel", layout="wide")
st.title("Web Excel (with Formulas)")


def load_data() -> pd.DataFrame:
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)

    return pd.DataFrame({column: ["", "", ""] for column in DEFAULT_COLUMNS})


def save_data(dataframe: pd.DataFrame) -> None:
    dataframe.to_csv(DATA_FILE, index=False)


def fn_sum(*args):
    return sum(args)


def fn_average(*args):
    return sum(args) / len(args) if args else 0


def fn_min(*args):
    return min(args)


def fn_max(*args):
    return max(args)


def fn_round(value, digits=0):
    return round(value, int(digits))


def fn_if(condition, true_value, false_value):
    return true_value if condition else false_value


def fn_and(*args):
    return all(args)


def fn_or(*args):
    return any(args)


def fn_not(value):
    return not value


def fn_len(text):
    return len(str(text))


def fn_concat(*args):
    return "".join(str(arg) for arg in args)


FUNCTIONS = {
    "SUM": fn_sum,
    "AVERAGE": fn_average,
    "MIN": fn_min,
    "MAX": fn_max,
    "ROUND": fn_round,
    "IF": fn_if,
    "AND": fn_and,
    "OR": fn_or,
    "NOT": fn_not,
    "LEN": fn_len,
    "CONCAT": fn_concat,
}


def replace_cell_references(formula: str, dataframe: pd.DataFrame) -> str:
    def replace_match(match: re.Match[str]) -> str:
        column_name = match.group(1)
        row_index = int(match.group(2)) - 1

        try:
            cell_value = dataframe.loc[row_index, column_name]
        except KeyError:
            return "0"
        except IndexError:
            return "0"

        if pd.isna(cell_value) or cell_value == "":
            return "0"

        try:
            number = float(cell_value)
            return str(int(number) if number.is_integer() else number)
        except (TypeError, ValueError):
            return "0"

    return re.sub(r"([A-Z])(\d+)", replace_match, formula)


def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def evaluate_formula(value, dataframe: pd.DataFrame):
    if not isinstance(value, str) or not value.startswith("="):
        return value

    formula = replace_cell_references(value[1:], dataframe)

    for function_name in FUNCTIONS:
        formula = re.sub(rf"\b{function_name}\b", f"FUNCTIONS['{function_name}']", formula)

    try:
        result = eval(formula, {"__builtins__": {}}, {"FUNCTIONS": FUNCTIONS})
        return format_result(result)
    except Exception:  # noqa: BLE001
        return "ERR"


def calculate_dataframe(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    result_dataframe = input_dataframe.copy()

    for column in result_dataframe.columns:
        for row_index in range(len(result_dataframe)):
            result_dataframe.loc[row_index, column] = evaluate_formula(
                input_dataframe.loc[row_index, column],
                input_dataframe,
            )

    return result_dataframe


raw_dataframe = load_data()
edited_dataframe = st.data_editor(
    raw_dataframe,
    num_rows="dynamic",
    use_container_width=True,
    key="mini_excel_editor",
)

calculated_dataframe = calculate_dataframe(edited_dataframe)

st.subheader("Calculated Result")
st.dataframe(calculated_dataframe, use_container_width=True)

if st.button("Save"):
    save_data(edited_dataframe)
    st.success("Saved.")

calculated_dataframe.to_excel(EXPORT_FILE, index=False)
with EXPORT_FILE.open("rb") as excel_file:
    st.download_button("Download Excel", excel_file, file_name="spreadsheet.xlsx")
