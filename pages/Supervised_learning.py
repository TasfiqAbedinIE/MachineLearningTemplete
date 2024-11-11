import pandas as pd
import streamlit as st
from joblib.parallel import method

from navigation import Side_Bar
from MachineLearningTemp import MachineLearningTemplete
import os
from io import BytesIO

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


# Downloading Data into excel file
def data_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data



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
                eliminated_dataframe = uploaded_dataframe


    except:
        pass

try:
    with st.expander("New Modified DataFrame"):
        st.dataframe(eliminated_dataframe, hide_index=True)
        # st.dataframe(eliminated_dataframe.isnull().sum())
    st.info("If you want to move forward with this data set PRESS SUBMIT. After submission if you want to change your any"
                " method, please start from the beginning.")
    missing_value_handled_dataset = eliminated_dataframe
    excel_data_missing_value = data_to_excel(missing_value_handled_dataset)
    st.download_button(
        label="Download data as Excel",
        data=excel_data_missing_value,
        file_name="output_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.success("Your Dataset is recorded and saved for the future use.")


except Exception as e:
    pass


st.divider()
st.markdown("<p class=section_title>DEPENDENT & INDEPENDENT VARIABLE SELECTION</p>", unsafe_allow_html=True)

# Section-4: Dependent & Independent variable selection --------------->
try:
    SEC4_R1_COL1, SEC4_R1_COL2 = st.columns(2)
    with SEC4_R1_COL1:
        selected_independent_variables = st.multiselect("Select Independent Variables", missing_value_handled_dataset.columns,
                                                        key="selected_independent_variables")
        st.info("Independent variables are those columns of your dataset which will be used to predict the future value of"
                " dependent variable.")
        independent_dataframe = missing_value_handled_dataset[selected_independent_variables]
        with st.expander("DataFrame of Independent Variables"):
            st.dataframe(independent_dataframe, hide_index=True, use_container_width=True)

    with SEC4_R1_COL2:
        selected_dependent_variable = st.multiselect("Select Dependent Variable",
                                                        missing_value_handled_dataset.columns,
                                                        key="selected_dependent_variables")
        st.info("Dependent variable is only column of your dataset which will be predicted based on the machine learning "
                "model your are going to choose for analysis.")
        dependent_dataframe = missing_value_handled_dataset[selected_dependent_variable]
        with st.expander("DataFrame of dependent Variables"):
            st.dataframe(dependent_dataframe, hide_index=True, use_container_width=True)

except Exception as e:
    # st.error("Please complete Previous sections FIRST")
    pass


st.divider()
st.markdown("<p class=section_title>CATEGORICAL DATA PROCESSING</p>", unsafe_allow_html=True)

# Section-5: categorical data processing --------------->

def independent_categorical_variables(independent_dataframe):
    st.markdown("<p style='font-weight: bold;'>Transforming Independent Variables</p>",
                unsafe_allow_html=True)
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np

    selected_independent_variables_cat = st.multiselect("Select Column name with categorical values",
                                                        independent_dataframe.columns,
                                                        key="selected_independent_variables_cat")

    try:
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
        concaneted_df = pd.DataFrame()
        # st.markdown(selected_independent_variables_cat)
        for item in selected_independent_variables_cat:
            column_data = independent_dataframe[[item]].values
            transformed_data = ct.fit_transform(column_data)
            transformed_data = pd.DataFrame(transformed_data)

            transformed_columns = transformed_data.columns
            column_name = []
            for i in range(len(transformed_columns)):
                column_name.append(item + f"_{str(i)}")

            transformed_data.columns = column_name
            concaneted_df = pd.concat([concaneted_df, transformed_data], axis=1)

        independent_dataframe_without_cat = independent_dataframe.drop(selected_independent_variables_cat, axis=1)
        independent_dataframe_for_ML = pd.concat([independent_dataframe_without_cat, concaneted_df], axis=1)
        with st.expander("Transformed Dataset of Independent Variables"):
            st.dataframe(independent_dataframe_for_ML, hide_index=True, use_container_width=True)
            return independent_dataframe_for_ML

    except Exception as e:
        st.error(e)

def dependent_categorical_variables(dependent_dataframe):
    st.markdown("<p style='font-weight: bold;'>Transforming Dependent Variables</p>",
                unsafe_allow_html=True)
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    try:
        dependent_columns = dependent_dataframe.columns
        dependent_columns = list(dependent_columns)

        dependent_column_name = []
        for i in dependent_columns:
            dependent_column_name.append(i)

        # st.markdown(dependent_column_name)

        dependent_column_data = dependent_dataframe[dependent_columns].values
        transformed_dependent_data = le.fit_transform(dependent_column_data)
        dependent_dataframe_for_ML = pd.DataFrame(transformed_dependent_data)
        dependent_dataframe_for_ML.columns = dependent_column_name

        with st.expander("Transformed Dataset of Dependent Variables"):
            st.dataframe(dependent_dataframe_for_ML, hide_index=True)
            return dependent_dataframe_for_ML

    except Exception as e:
        st.error(e)


try:
    if dependent_dataframe and independent_dataframe:
        st.info("If your dataset contains categorical values, it is important to transform those into numerical values.")
        # selected_caltegorical_columns = st.multiselect("Select Categorical Columns", independent_dataframe.columns,
        #                                                key="selected_categorical_columns")
        question_for_transformation = st.radio("Does you dataset contains categorical values?", ["YES", "NO"], index=None,
                                                key="question_for_transformation")
        if question_for_transformation == "YES":
            st.markdown("<p style='margin-top: 2vh; font-weight: bold; font-size:20px'>Select Variables contains categorical value</p>",
                            unsafe_allow_html=True)

            independent_variable_for_cat = st.checkbox("Independent Variables", key="independent_variable_for_cat")
            dependent_variable_for_cat = st.checkbox("Dependent Variables", key="dependent_variable_for_cat")

            if independent_variable_for_cat:
                independent_dataframe_for_ML = independent_categorical_variables(independent_dataframe)
            else:
                independent_dataframe_for_ML = independent_dataframe

            if dependent_variable_for_cat:
                dependent_dataframe_for_ML = dependent_categorical_variables(dependent_dataframe)
            else:
                dependent_dataframe_for_ML = dependent_dataframe


        if question_for_transformation == "NO":
            independent_dataframe_for_ML = independent_dataframe
            dependent_dataframe_for_ML = dependent_dataframe
            st.success("You are ready to develop machine learning model. Move forward to the Next Section.")


except Exception as e:
    pass

