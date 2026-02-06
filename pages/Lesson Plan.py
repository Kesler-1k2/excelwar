import streamlit as st




st.write("success showing")
st.set_page_config(page_title="Excel Lesson Plan", page_icon="📊")

st.title("📊 Excel 3-Lesson Plan")

st.write("This app provides an overview of three Excel lessons and their summaries.")

# Create tabs
lesson1, lesson2, lesson3 = st.tabs(["Lesson 1", "Lesson 2", "Lesson 3"])

# Lesson 1
with lesson1:
    st.header("Lesson 1: Introduction to Excel & Basic Functions")

    st.subheader("Summary")
    st.write("""
    Students learn the purpose of Excel and how to navigate the interface. 
    They practise entering and formatting data and use basic formulas such as 
    SUM, AVERAGE, MIN, and MAX to perform simple calculations.
    """)

    st.subheader("Key Topics")
    st.write("""
    - Excel interface (rows, columns, cells)
    - Entering and formatting data
    - Basic formulas
    """)

# Lesson 2
with lesson2:
    st.header("Lesson 2: Data Organisation & Formatting Tools")

    st.subheader("Summary")
    st.write("""
    Students learn how to organise data using sorting and filtering. 
    They also apply conditional formatting to highlight important information 
    and understand the difference between relative and absolute cell referencing.
    """)

    st.subheader("Key Topics")
    st.write("""
    - Sorting and filtering data
    - Conditional formatting
    - Cell referencing
    """)

# Lesson 3
with lesson3:
    st.header("Lesson 3: Charts & Practical Application")

    st.subheader("Summary")
    st.write("""
    Students learn how to create and customise charts to present data visually. 
    They apply their knowledge by completing a small project using Excel to 
    organise, analyse, and present data.
    """)

    st.subheader("Key Topics")
    st.write("""
    - Creating charts
    - Chart customisation
    - Real-world Excel project
    """)

st.success("Select a lesson tab above to view its content.")