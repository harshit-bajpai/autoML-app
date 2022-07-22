import logging
import sys
import traceback

import pandas as pd
import streamlit as st

PAGE_NAME = "3_Preprocess_Data"

def preprocess_data_st(df):
    from database.preprocess_data import PreprocessData

    preprocessObj = PreprocessData(df)
    non_numeric = preprocessObj.handle_non_numeric()
    st.text(["Non-numeric features not found!" if type(non_numeric) is None else f"Non-numeric features dropped : {non_numeric}"])
    ms_values_dict = preprocessObj.handle_missing_values()
    if "cols_drop" in ms_values_dict.keys():
        st.text(f"{ms_values_dict['cols_drop']}")
    st.text(["Missing values not found!" if "drop_na" in ms_values_dict.keys() else f"{ms_values_dict['drop_na']}"])
    st.text(f"Split data with {preprocessObj.test_ratio} test ratio.")
    X_train, X_test, y_train, y_test = preprocessObj.split_data()
    st.text(f"X_train shape: {X_train.shape}")
    st.text(f"X_test shape: {X_test.shape}")
    scale_method = st.selectbox("Select a method:", ["MinMax", "Standard", "MinMax"])
    X_train, X_test = preprocessObj.scale_data(X_train, X_test, scale_method.lower())
    st.text(f"Scaled data with {scale_method} scaling.")
    st.session_state["X_train"] = X_train.to_dict()
    st.session_state["y_train"] = y_train.to_dict()
    st.session_state["X_test"] = X_test.to_dict()
    st.session_state["y_test"] = y_test.to_dict()
    logging.debug("Preprocess Data object data generation completed.")
    logging.debug("Dataframes stored in session state.")

def setup_page_skeleton():
    try:
        st.set_page_config(page_title="Preprocess Data", page_icon="👀", layout="wide")
        st.markdown("# 👀 Preprocessing Data")
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.")
        logging.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.\
            \n{err}\n{traceback.format_exc()}")

def main():
    try:
        setup_page_skeleton()
        if st.button("▶️ Preprocess Data"):
            if "data" in st.session_state:
                df = pd.DataFrame(st.session_state["data"])
                with st.container():
                        st.subheader("Preprocess Dataset for model development")
                        preprocess_data_st(df)
            else:
                exp = RuntimeError("Data not found. Please ensure you have uploaded a dataset.")
                st.exception(exp)
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error in the main method.")
        logging.error(f"{PAGE_NAME} page ran into an error in the main method.\n{err}\n{traceback.format_exc()}")


if __name__ == "__main__":
    sys.path.insert(1, "./database/")
    main()
