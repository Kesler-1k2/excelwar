import pandas as pd
import streamlit as st

st.title("Practices")
st.write("Use this page to practice editing spreadsheet data.")

practice_df = pd.DataFrame(
    {
        "Task": ["Enter data", "Use SUM", "Create chart"],
        "Status": ["Not started", "Not started", "Not started"],
    }
)

edited_df = st.data_editor(practice_df, num_rows="dynamic", use_container_width=True)
st.subheader("Your Practice Table")
st.dataframe(edited_df, use_container_width=True)
