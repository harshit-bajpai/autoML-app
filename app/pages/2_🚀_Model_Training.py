import sys

import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="Model Training", page_icon="🚀", layout="wide")
    st.markdown("# Model Training")
    return

def main():

    setup_page_skeleton()
    return

if __name__ == "__main__":
    sys.path.insert(1, "../modelDev/")
    main()