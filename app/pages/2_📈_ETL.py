import sys
import time

import streamlit as st
import pandas as pd


def setup_page_skeleton():
    try:
        st.set_page_config(page_title="ETL", page_icon="📈", layout="wide")
        st.markdown("# 📈 Extract, Transform, Load")
        experiment_name = st.text_input("Enter experiment name:", "", 16)
        if experiment_name != "":
            st.session_state["experiment_name"] = experiment_name
            st.session_state["runtime_start"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            return experiment_name
        else:
            exp = KeyError("Experiment name is empty")
            st.exception(exp)
            return None
    except Exception as err:
        st.error(f"Page 2 ran into an error while setting up skeleton")
        return ""

def build_data_st(experiment_name):
    from buildData import buildData

    dataObj = buildData(experiment_name)
    df = dataObj.data
    
    with st.container():
        st.subheader("Build data configuration:")
        n_samples = st.number_input("Number of samples", 100, 100000, 100, 100)
        n_features = st.number_input("Number of features", 20, 1000, 20, 5)
        n_informative = st.number_input("Number of informative features", 10, 500, 10, 10)
        n_targets = 1 # the applicaion only supports one target
        noise = st.number_input("Noise", 0.0, 1.0, 0.0, 0.1)
        timestamp_col = st.checkbox("Add timestamp column", False)
        id_col = st.checkbox("Add id column", False)

    if st.button("▶️ Run"):
        t = time.time()
        df = dataObj.regression_data(n_samples=n_samples, n_features=n_features, 
            n_informative=n_informative, n_targets=n_targets, noise=noise, 
            id_col=id_col, timestamp_col=timestamp_col)
        st.write(f"Runtime: {time.time()-t:.3f} seconds")
        st.session_state["data"] = df.to_dict()

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
        experiment_name= setup_page_skeleton()
        if experiment_name is not None:
            option = st.selectbox("Select an option:", ["Build data", "Load data"], index=1)
            if (option == "Build data"):
                df = build_data_st(experiment_name)
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
    except Exception as err:
        st.error(f"Page 2 ran into an error in main")

if __name__ == "__main__":
    sys.path.insert(1, "./database/")
    main()