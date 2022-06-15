import sys
import time

import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="ETL", page_icon="📈", layout="wide")
    st.markdown("# 📈 Extract, Transform, Load")
    experiment_name = st.text_input("Enter experiment name:", "fuzzy_bohr", 16)

    return experiment_name

def build_data(experiment_name):
    from buildData import buildData

    dataObj = buildData(experiment_name)
    
    with st.container():
        st.subheader("Build data configuration:")
        n_samples = st.number_input("Number of samples", 100, 100000, 100, 100)
        n_features = st.number_input("Number of features", 20, 1000, 20, 5)
        n_informative = st.number_input("Number of informative features", 10, 500, 10, 10)
        n_targets = 1 # the applicaion only supports one target
        noise = st.number_input("Noise", 0.0, 1.0, 0.0, 0.1)

    if st.button("▶️ Run"):
        t = time.time()
        df = dataObj.sklearn_regression_data(n_samples, n_features, 
            n_informative, n_targets, noise=noise)
        st.write(f"Runtime: {time.time()-t:.2f} seconds")

        with st.container():
            st.subheader("Data profile:")
            st.write(f"Shape of data: {df.shape}")
            st.write("Dataframe head:")
            st.dataframe(df.head())
            st.write("Dataframe descriptive statistics:")
            st.dataframe(df.describe().transpose())

def main():

    experiment_name= setup_page_skeleton()
    option = st.selectbox("Select an option:", ["Build data", "Load data"], index=1)

    if option == "Build data":
        build_data(experiment_name) 
    elif option == "Load data":
        st.write("Load data functionality coming soon!")
        with st.expander("Format of data required for loading it to the application"):
            st.write("""
                The data must be in a CSV file with the following columns:
                - `id`: unique identifier for each sample
                - `target`: the target value
                - `feature_1`: the first feature
                - `feature_2`: the second feature
                - `feature_3`: the third feature
                ......
                - `feature_n`: the nth feature
            """)

    return

if __name__ == "__main__":
    sys.path.insert(1, "../database/")
    main()