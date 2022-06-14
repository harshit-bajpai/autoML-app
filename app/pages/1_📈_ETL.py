import sys
import time

import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="ETL", page_icon="📈", layout="wide")
    st.markdown("# ETL Data")
    return

def build_data():
    from buildData import buildData

    experiment_name = st.text_input("Enter experiment name:", "fuzzy_bohr", 16)
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

    setup_page_skeleton()
    build_data() 

    return

if __name__ == "__main__":
    sys.path.insert(1, "../database/")
    main()