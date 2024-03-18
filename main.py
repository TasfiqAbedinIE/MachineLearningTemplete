import streamlit as st
from MachineLearningTemp import MachineLearningTemplete


main_window = MachineLearningTemplete()

data_file = main_window.file_uploader()

main_window.display_dataframe(data_file)

