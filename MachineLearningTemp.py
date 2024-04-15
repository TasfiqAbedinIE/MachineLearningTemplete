import streamlit as st
import pandas as pd


class MachineLearningTemplete:
    def __init__(self):
        super().__init__()
        st.markdown("<p style='font-size: 36px; font-weight: bold; color: #8338ec; text-align: center'>Machine Learning Model</p>", unsafe_allow_html=True)
        self.display_complete = False


    def file_uploader(self):
        data_file = st.file_uploader("Upload Your File", key="Main Data File", help="Only CSV file is supported")
        return data_file

    def display_dataframe(self, data_file):
        if data_file:
            dataset = pd.read_csv(data_file)
            st.markdown("<p style='font-size: 24px; font-weight: bold; color: #5f5ff6'>Uploaded Dataset</p>", unsafe_allow_html=True)
            st.dataframe(dataset, hide_index=True, use_container_width=True)
            self.columns_name = dataset.columns
            c1, c2 = st.columns([3,1])
            with c1:
                st.markdown("<p style='font-size: 24px; font-weight: bold; color: #5f5ff6'>Select Column Name to Finalize your Dataset</p>", unsafe_allow_html=True)
                self.selected_column_for_main_data_set = st.multiselect("Column List", self.columns_name)
                if len(self.selected_column_for_main_data_set) != 0:
                    self.main_data_set = dataset[self.selected_column_for_main_data_set]
                else:
                    self.main_data_set = dataset

            main_data_show = st.expander("Final Dataset")
            with main_data_show:
                st.dataframe(self.main_data_set, hide_index=True, use_container_width=True)
                self.display_complete = True
        else:
            pass

    def check_for_missing_values(self):
        missing_value_columns = self.main_data_set.isnull().sum()
        return missing_value_columns

    def working_with_missing_values(self):
        st.markdown("<p style='font-size: 24px; font-weight: bold; color: #5f5ff6'>Working With Missing Values</p>", unsafe_allow_html=True)
        check_missing_values = st.checkbox("Check for Missing Values", key= "missing_values")
        if check_missing_values:
            missing_value_columns = self.check_for_missing_values()
            c1, c2 = st.columns([1, 3])
            with c1:
                st.dataframe(missing_value_columns, hide_index=True, use_container_width=True, column_config={
                    0: st.column_config.Column("Name of Variables"),
                    1: st.column_config.Column("Sum of Missing Values")
                })
            with c2:
                st.radio("Select Method to handle Missing Values", ["By Eliminating", "By MEAN and MAX Values"],key="missing_value_handling_tech", horizontal=True, index=None)





