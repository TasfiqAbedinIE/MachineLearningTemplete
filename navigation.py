import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


class Side_Bar:
    def __init__(self):
        super().__init__()

    def get_current_page_name(self):
        ctx = get_script_run_ctx()
        if ctx is None:
            raise RuntimeError("Couldn't get script context")

        pages = get_pages("")

        return pages[ctx.page_script_hash]["page_name"]

    def make_sidebar(self):
        with st.sidebar:
            st.markdown(f"<p style='font-size: 24px; font-weight: bold; color: #fff'>MACHINE LEARNING TEMPLATE</p>", unsafe_allow_html=True)
            st.markdown("")
            st.page_link("pages/Supervised_learning.py", label="SUPERVISED LEARNING", icon=":material/empty_dashboard:")











