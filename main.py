import streamlit as st
from navigation import Side_Bar
from data_upload_preprocessing import data_upload

class streamlit_page_config:
    st.set_page_config(
        page_title="MACHINE LEARNING TEMPLATE",
        layout= "wide",
        initial_sidebar_state='auto',

    )
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    hide_footer_style = '''<style>.reportview-container .main footer {visibility: hidden;} </style>'''
    st.markdown(hide_footer_style, unsafe_allow_html=True)
    hide_menu_style = '''<style> #MainMenu {visibility: hidden;} </style>'''
    st.markdown(hide_menu_style, unsafe_allow_html=True)


streamlit_page_config()
side_bar = Side_Bar()
side_bar.make_sidebar()

user_info = "This is a boiler plate Machine learning template and focused to apply machine learning methods to basic stage. I wanted to built it so that people with no coding skill can apply Machine Learning into their dataset with minimum effort."

# Section-1: Uploading the DATASET --------------->
st.markdown("<p class=section_title>DATA UPLOAD</p>", unsafe_allow_html=True)
raw_data_file = st.file_uploader("File Upload", type=["xlsx", "csv"], key="raw_data_file")
if raw_data_file:
    pass
else:
    st.info(user_info)

