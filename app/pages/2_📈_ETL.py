"""
ETL page for the application.
"""
import logging
import sys
import time
import traceback

import pandas as pd
import streamlit as st

PAGE_NAME = "2_ETL"

def setup_page_skeleton():
    try:

        st.set_page_config(page_title="ETL", page_icon="📈", layout="wide")
        st.markdown("# 📈 Extract, Transform, Load")
        
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.")
        logging.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.\
            \n{err}\n{traceback.format_exc()}")
        return ""

def build_data_st(experiment_name):
    from database.build_data import BuildData

    dataObj = BuildData(experiment_name)
    df = dataObj.data
    logging.info(f"buildData object generated.")
    timestamp_col = False
    id_col = False
    
    with st.container():
        st.subheader("Build data configuration:")
        n_samples = st.number_input("Number of samples", 100, 100000, 100, 100)
        n_features = st.number_input("Number of features", 20, 1000, 20, 5)
        n_informative = st.number_input("Number of informative features", 10, 500, 10, 10)
        n_targets = 1 # the application only supports one target
        noise = st.number_input("Noise", 0.0, 1.0, 0.0, 0.1)
        timestamp_col = st.checkbox("Add timestamp column", False)
        id_col = st.checkbox("Add id column", False)

    if st.button("▶️ Run"):
        t = time.time()
        logging.info(f"buildData object data generation started.")
        df = dataObj.regression_data(n_samples=n_samples, n_features=n_features, 
            n_informative=n_informative, n_targets=n_targets, noise=noise, 
            id_col=id_col, timestamp_col=timestamp_col) 
        logging.info(f"buildData object data generation completed in {time.time() - t:.3f} seconds.")
        logging.info(f"Dataframe generated with {df.shape[0]} rows and {df.shape[1]} columns.")
        st.write(f"Runtime: {time.time()-t:.3f} seconds")
        st.session_state["data"] = df.to_dict()
        logging.info(f"Dataframe stored in session state.")

        with st.container():
            st.subheader("Data profile:")
            st.write(f"Shape of data: {df.shape}")
            st.session_state["data_shape"] = str(list(df.shape))
            st.session_state["n_features"] = n_features
            st.session_state["n_targets"] = n_targets
            if timestamp_col:st.session_state["timestamp_col"] = "timestamp"
            if id_col:st.session_state["id_col"] = "id"
            st.session_state["id_col"] = id_col
            st.session_state["timestamp_col"] = timestamp_col
            st.write("Dataframe head:")
            st.dataframe(df.head())
            st.write("Dataframe descriptive statistics:")
            st.dataframe(df.describe().transpose())
        return df
    else:
        return df

def main():
    try:
        setup_page_skeleton()
    
        if 'experiment_name' in st.session_state:
            option = st.selectbox("Select an option:", ["Build data", "Load data"], index=1)
            if (option == "Build data"):
                df = build_data_st(st.session_state["experiment_name"])
                st.session_state["data_generator"] = "buildData"
                # if not df.empty:
                    # prepare data for model training
            elif option == "Load data":
                st.write("Load data functionality coming soon!")
                st.session_state["data_generator"] = "loadData"
                with st.expander("Format of data required for loading it to the application"):
                    st.write("""
                        The data must be in a CSV file with the following columns:
                        - `id`: unique identifier for each sample, for eg. `timestamp`
                        - `target`: the target value
                        - `feature_1`: the first feature
                        - `feature_2`: the second feature
                        - `feature_3`: the third feature
                        ......
                        - `feature_n`: the nth feature
                        Assumptions:
                        -  the id column will be assumed equivalent to timestamp. If both are present, the id column will be prioritized.
                    """)
        else:
            exp = RuntimeError("Please ensure you run the previous pages.")
            st.exception(exp)
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error in the main method.")
        logging.error(f"{PAGE_NAME} page ran into an error in the main method.\n{err}\n{traceback.format_exc()}")

if __name__ == "__main__":
    sys.path.insert(1, "./")
    main()
