import sys

import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="Model Evaluation", page_icon="👀", layout="wide")
    st.markdown("# Model Evaluation")
    return

def main():

    setup_page_skeleton()
    return

if __name__ == "__main__":
    sys.path.insert(1, "../modelDev/")
    main()