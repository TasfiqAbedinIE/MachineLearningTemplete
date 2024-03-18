import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Machine Learning Templete",
    layout="wide",
    initial_sidebar_state="collapsed",
)


class MachineLearningTemplete:
    def __init__(self):
        super().__init__()
        st.markdown("Machine Learning Templete")


    def file_uploader(self):
        data_file = st.file_uploader("Upload Your File", key="Main Data File", help="Only CSV file is supported")
        return data_file

    def display_dataframe(self, data_file):
        if data_file:
            dataset = pd.read_csv(data_file)
            st.markdown("Uploaded Dataset")
            st.dataframe(dataset, hide_index=True, use_container_width=True)
        else:
            pass


