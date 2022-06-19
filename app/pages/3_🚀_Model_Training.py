import sys
import json

import pandas as pd
from sklearn import datasets
import streamlit as st


def setup_page_skeleton():
    st.set_page_config(page_title="Model Training", page_icon="🚀", layout="wide")
    st.markdown("# Model Training")
    data = pd.DataFrame(st.session_state["data"])
    st.dataframe(data.head())
    return

def main():

    setup_page_skeleton()
    return

if __name__ == "__main__":
    sys.path.insert(1, "./modelDev/")
    main()