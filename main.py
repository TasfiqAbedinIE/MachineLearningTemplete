import streamlit as st
from MachineLearningTemp import MachineLearningTemplete

st.set_page_config(
    page_title="Machine Learning Templete",
    layout="wide",
    initial_sidebar_state="collapsed",
)


main_window = MachineLearningTemplete()

data_file = main_window.file_uploader()
main_window.display_dataframe(data_file)

if main_window.display_complete:
    main_window.working_with_missing_values()
