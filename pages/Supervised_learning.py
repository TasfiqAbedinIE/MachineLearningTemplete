import pandas as pd
import streamlit as st
from joblib.parallel import method

from navigation import Side_Bar
from MachineLearningTemp import MachineLearningTemplete
import os

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
def file_type_varification(file):
    _, file_ext = os.path.splitext(file.name)
    file_type = file_ext[1:]

    if file_type == "csv":
        uploaded_dataframe = pd.read_csv(raw_data_file)
        dataframe_uploaded = True
    elif file_type == "xlsx":
        excel_sheetname = st.text_input("Enter Sheet Name", key="excel_sheetname")
        if excel_sheetname:
            uploaded_dataframe = pd.read_excel(raw_data_file, sheet_name=excel_sheetname)
            dataframe_uploaded = True
    else:
        st.error("File type is not supported.")

    return uploaded_dataframe


st.markdown("<p class=section_title>DATA UPLOAD SECTION</p>", unsafe_allow_html=True)
raw_data_file = st.file_uploader("File Upload", type=["xlsx", "csv"], key="raw_data_file")
if raw_data_file:
   uploaded_dataframe = file_type_varification(raw_data_file)
   if uploaded_dataframe is not None:
       with st.expander("DATA FRAME"):
           st.dataframe(uploaded_dataframe, hide_index=True)
else:
    st.info(user_info)


# Section-2: Evaluating Descriptive Statistics --------------->
def descriptive_stat(uploaded_dataframe):
    description_of_dataframe = uploaded_dataframe.describe()

    return description_of_dataframe

try:
    if uploaded_dataframe is not None:
        description_of_dataframe = descriptive_stat(uploaded_dataframe)
        with st.expander("DESCRIPTIVE STATISTICS"):
            st.dataframe(description_of_dataframe, use_container_width=True)
except:
    pass

st.divider()
st.markdown("<p class=section_title>DATA PREPARATION SECTION</p>", unsafe_allow_html=True)

# Section-3: Handling Missing values --------------->

def by_eliminating(uploaded_dataframe):
    eliminated_dataframe = uploaded_dataframe.dropna(subset=columns_of_missing_values)
    return eliminated_dataframe

def by_mean_median(uploaded_dataframe, columns):
    dataframe_to_modify = uploaded_dataframe
    eliminated_dataframe = uploaded_dataframe[columns].fillna(uploaded_dataframe[columns].mean())
    dataframe_to_modify[columns] = eliminated_dataframe
    return dataframe_to_modify

def by_imputation(uploaded_dataframe, imputation_method):
    if imputation_method == "Forward Fill":
        imp_meth = 'ffill'
    else:
        imp_meth = 'bfill'

    eliminated_dataframe = uploaded_dataframe.fillna(method=imp_meth)
    return eliminated_dataframe

def by_interpolation(uploaded_dataframe, interpolation_method, columns):
    dataframe_to_modify = uploaded_dataframe
    if interpolation_method == "linear":
        eliminated_dataframe = dataframe_to_modify[columns].interpolate(method=interpolation_method)
    elif interpolation_method == "time":
        eliminated_dataframe = dataframe_to_modify[columns].interpolate(method=interpolation_method)
    elif interpolation_method == "polynomial":
        eliminated_dataframe = dataframe_to_modify[columns].interpolate(method=interpolation_method, order=2)
    elif interpolation_method == "spline":
        eliminated_dataframe = dataframe_to_modify[columns].interpolate(method=interpolation_method, order=2)
    elif interpolation_method == "nearest":
        eliminated_dataframe = dataframe_to_modify[columns].interpolate(method=interpolation_method)

    dataframe_to_modify[columns] = eliminated_dataframe
    return dataframe_to_modify


def finding_missing_value(uploaded_dataframe):
    null_calculation = uploaded_dataframe.isnull().sum().to_frame("Total Missing Values")
    null_calculation.index.name = "Column Name"
    null_calculation.reset_index()

    return null_calculation

sec3_r1c1, sec3_r1c2 = st.columns([4, 6])
with sec3_r1c1:
    try:
        if uploaded_dataframe is not None:
            check_for_missing_values = st.checkbox("CHECK FOR MISSING VALUES?", key="check_for_missing_values")
            if check_for_missing_values:
                try:
                    null_calculation = finding_missing_value(uploaded_dataframe)
                    st.markdown("<p style='font-weight: bold'>MISSING VALUES</p>", unsafe_allow_html=True)
                    st.dataframe(null_calculation, use_container_width=True)
                except:
                    pass
        else:
            pass
    except:
        pass

with sec3_r1c2:
    try:
        if check_for_missing_values:
            st.markdown("<p style='margin-top: 10vh; font-weight: bold;'>Do you want to take care of missing values?</p>",
                        unsafe_allow_html=True)
            caring_missing_value_permission = st.radio("", ["YES", "NO"], key="caring_missing_value_permission",
                                                       label_visibility="collapsed", index=None)
            if caring_missing_value_permission == "YES":
                method_of_data_preparation = st.selectbox("Data Preparation Methods", ["By Eliminating", "By MEAN and MAX Values",
                                                                                       "Imputation Method", "Interpolation Method"],
                                                          key="method_of_data_preparation")
                columns_of_dataframe = uploaded_dataframe.columns
                # By Elimination ------------------>>>>
                if method_of_data_preparation == "By Eliminating":
                    columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
                                                            key="columns_of_missing_values")
                    try:
                        eliminated_dataframe = by_eliminating(uploaded_dataframe)
                        count_original_rows = len(uploaded_dataframe)
                        count_eliminated_rows = len(eliminated_dataframe)
                        st.warning(f"You Lost {((count_original_rows-count_eliminated_rows)/count_original_rows)*100:.2f} % of original data")

                    except Exception as e:
                        st.error(e)

                # By MEAN and MAX Values ------------------>>>>
                if method_of_data_preparation == "By MEAN and MAX Values":
                    st.info("If missing values column contains categorical values, MEAN & MAX Method will results error. Please choose"
                            " columns with only numerical values.")
                    columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
                                                               key="columns_of_missing_values")
                    try:
                        eliminated_dataframe = by_mean_median(uploaded_dataframe, columns_of_missing_values)
                    except Exception as e:
                        st.error("Failed to Fill Missing values.")

                # By Imputation Method ------------------>>>>
                if method_of_data_preparation == "Imputation Method":
                    st.info(
                        "If your have a big dataset and there are loads of correlation amongst your data variables,"
                        " this method may change the behavior of your dataset.")
                    imputation_method = st.selectbox("Select Imputation Method", ["Forward Fill", "Backward Fill"],
                                                     key="Imputation_method_selection")

                    try:
                        eliminated_dataframe = by_imputation(uploaded_dataframe, imputation_method)
                    except Exception as e:
                        st.error(e)

                # By Interpolation Method ------------------>>>>
                if method_of_data_preparation == "Interpolation Method":
                    st.info(
                        "If your missing values are categorical DO NOT USE this method,"
                        " it will not bring anything good out of it.")

                    interpolation_method = st.selectbox("Select Interpolation Method", ["linear", "time", "polynomial", "spline", "nearest"],
                                                     key="Interpolation_method_selection")
                    columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
                                                               key="columns_of_missing_values")

                    try:
                        eliminated_dataframe = by_interpolation(uploaded_dataframe, interpolation_method, columns_of_missing_values)
                    except Exception as e:
                        st.error(e)



            elif caring_missing_value_permission == "NO":
                st.info("Let's Move Forward With Your Existing DataFrame.")


    except:
        pass

try:
    with st.expander("New Modified DataFrame"):
        st.dataframe(eliminated_dataframe, hide_index=True)
        # st.dataframe(eliminated_dataframe.isnull().sum())
    st.info("If you want to move forward with this data set PRESS SUBMIT. After submission if you want to change your any"
                " method, please start from the beginning.")
    if st.button("SUBMIT"):
        pass

except Exception as e:
    pass
#
#
#
#                 try:
#                     # Handling Missing Values using MEAN, MEDIAN, MODE Method ----->
#                     if method_of_data_preparation == "By MEAN and MAX Values":
#                         st.info("If missing values column contains categorical values, MEAN & MAX Method will results error. If you don't"
#                                 " want to lose values of your dataframe you can move forward and transform the categorical values before"
#                                 " applying the method.")
#
#                         columns_of_missing_values = st.multiselect("Select Columns to Apply Method:", columns_of_dataframe,
#                                                                    key="columns_of_missing_values")
#                         st.markdown(columns_of_missing_values)
#                 except Exception as e:
#                     st.error(e)



                # Imputation Method ----->
                # df.fillna(value=0, inplace=True)  # Replace with 0
                # df.fillna(method='ffill', inplace=True)  # Forward-fill missing values
                # df.fillna(method='bfill', inplace=True)  # Backward-fill missing values

                # Interpolation Method ----->
                # df.interpolate(method='linear', inplace=True)  # Linear interpolation

#             if caring_missing_value_permission == "NO":
#                 st.info("HORRAAA!!! Let's Move Forward With Your Existing DataFrame.")
# except:
#     pass







