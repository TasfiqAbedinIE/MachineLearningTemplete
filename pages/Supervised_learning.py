import pandas as pd
import streamlit as st
from navigation import Side_Bar
from MachineLearningTemp import MachineLearningTemplete

class streamlit_page_config:
    st.set_page_config(
        page_title="MACHINE LEARNING TEMPLATE",
        layout= "wide",
        initial_sidebar_state='auto',

    )
    st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

    hide_footer_style = '''<style>.reportview-container .main footer {visibility: hidden;} </style>'''
    st.markdown(hide_footer_style, unsafe_allow_html=True)
    hide_menu_style = '''<style> #MainMenu {visibility: hidden;} </style>'''
    st.markdown(hide_menu_style, unsafe_allow_html=True)


streamlit_page_config()
side_bar = Side_Bar()
side_bar.make_sidebar()

user_info = "This is a boiler plate Machine learning template and focused to apply machine learning methods to basic stage. I wanted to built it so that people with no coding skill can apply Machine Learning into their dataset with minimum effort."
dataframe_uploaded = False

# Section-1: Uploading the DATASET --------------->
st.markdown("<p class=section_title>DATA UPLOAD</p>", unsafe_allow_html=True)
raw_data_file = st.file_uploader("File Upload", type=["xlsx", "csv"], key="raw_data_file")
if raw_data_file:
    MC_Template = MachineLearningTemplete(raw_data_file)
    file_type = MC_Template.check_file_ext()

    if file_type == "csv":
        with st.expander("DATA FRAME"):
            uploaded_dataframe = pd.read_csv(raw_data_file)
            st.dataframe(uploaded_dataframe, hide_index=True, use_container_width=True)
            dataframe_uploaded = True
    elif file_type == "xlsx":
        excel_sheetname = st.text_input("Enter Sheet Name", key="excel_sheetname")
        if excel_sheetname:
            with st.expander("DATA FRAME"):
                uploaded_dataframe = pd.read_excel(raw_data_file, sheet_name=excel_sheetname)
                st.dataframe(uploaded_dataframe, hide_index=True, use_container_width=True)
                dataframe_uploaded = True
    else:
        st.error("File type is not supported.")

else:
    st.info(user_info)


# Section-2: Evaluating Descriptive Statistics --------------->
try:
    if file_type != None and dataframe_uploaded:
        with st.expander("DESCRIPTIVE STATISTICS"):
            description_of_dataframe = uploaded_dataframe.describe()
            st.dataframe(description_of_dataframe, use_container_width=True)
except:
    pass

# Section-3: Handling Missing values --------------->
MV_r1c1, MV_r1c2 = st.columns([4, 6])
with MV_r1c1:
    check_for_missing_values = st.checkbox("CHECK FOR MISSING VALUES?", key="check_for_missing_values")
    if check_for_missing_values:
        try:
            st.markdown("<p style='font-weight: bold'>MISSING VALUES</p>", unsafe_allow_html=True)
            null_calculation = uploaded_dataframe.isnull().sum().to_frame("Total Missing Values")
            null_calculation.index.name = "Column Name"
            null_calculation.reset_index()
            st.dataframe(null_calculation, use_container_width=True)
        except:
            pass

if check_for_missing_values:
    with MV_r1c2:
        st.markdown("<p style='margin-top: 10vh; font-weight: bold;'>Do you want to take care of missing values?</p>",
                    unsafe_allow_html=True)
        caring_missing_value_permission = st.radio("", ["YES", "NO"], key="caring_missing_value_permission",
                                                   label_visibility="collapsed", index=None)
        if caring_missing_value_permission == "YES":
            method_of_data_preparation = st.selectbox("Data Preparation Methods", ["By Eliminating", "By MEAN and MAX Values"],
                                                      key="method_of_data_preparation")
            columns_of_dataframe = uploaded_dataframe.columns

            # Handling Missing Values by Eliminating ----->
            if method_of_data_preparation == "By Eliminating":
                columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
                                                           key="columns_of_missing_values")
                try:
                    uploaded_dataframe.dropna(subset=columns_of_missing_values, inplace=True)
                except:
                    st.warning("Select Columns to Eliminate Missing values from columns.")

            # Handling Missing Values using MEAN, MEDIAN, MODE Method ----->
            if method_of_data_preparation == "By MEAN and MAX Values":
                st.info("If missing values column contains categorical values, MEAN & MAX Method will results error. If you don't"
                        " want to lose values of your dataframe you can move forward and transform the categorical values before"
                        " applying the method.")

                columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
                                                           key="columns_of_missing_values")
                st.markdown(columns_of_missing_values)

            # Imputation Method ----->
            # df.fillna(value=0, inplace=True)  # Replace with 0
            # df.fillna(method='ffill', inplace=True)  # Forward-fill missing values
            # df.fillna(method='bfill', inplace=True)  # Backward-fill missing values

            # Interpolation Method ----->
            # df.interpolate(method='linear', inplace=True)  # Linear interpolation

        if caring_missing_value_permission == "NO":
            st.info("HORRAAA!!! Let's Move Forward With Your Existing DataFrame.")


st.dataframe(uploaded_dataframe.isnull().sum())




