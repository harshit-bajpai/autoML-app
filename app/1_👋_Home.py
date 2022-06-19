import logging

import streamlit as st

if "shared" not in st.session_state:
   st.session_state["shared"] = True

st.set_page_config(page_title="autoML", page_icon="👋", layout="wide")

st.write("# AutoML Application👋")

st.sidebar.success("Welcome to the AutoML application! \
                    Please go through the options in the sidebar sequently.")

st.markdown(
    """
    ---
    
    ## Minimum Viable Product(MVP)

    ### Supported Features:

    - [ ] ETL
    - [ ] Model Training
    - [ ] Model Evaluation
    - [ ] Export Configuration

    """
    )