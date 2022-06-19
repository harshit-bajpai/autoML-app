import sys
import time

import streamlit as st
import pandas as pd


def setup_page_skeleton():

    st.set_page_config(page_title="ETL", page_icon="📈", layout="wide")
    st.markdown("# 📈 Extract, Transform, Load")
    experiment_name = st.text_input("Enter experiment name:", "", 16)
    if experiment_name != "":
        st.session_state["experiment_name"] = experiment_name
        st.session_state["runtime_start"] = time.time()
        return experiment_name

def build_data(experiment_name):
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

    if st.button("▶️ Run"):
        t = time.time()
        df = dataObj.sklearn_regression_data(n_samples, n_features, 
            n_informative, n_targets, noise=noise)
        st.write(f"Runtime: {time.time()-t:.2f} seconds")
        st.session_state["data"] = df.to_dict()

        with st.container():
            st.subheader("Data profile:")
            st.write(f"Shape of data: {df.shape}")
            st.session_state["data_shape"] = str(list(df.shape))
            st.session_state["n_features"] = n_features
            st.session_state["n_targets"] = n_targets
            st.write("Dataframe head:")
            st.dataframe(df.head())
            st.write("Dataframe descriptive statistics:")
            st.dataframe(df.describe().transpose())
        return df
    else:
        return df

def preprocessing_data(df):
    st.subheader("Preprocessing data")
    
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    st.session_state["scaler"] = scaler
    df_transform = scaler.fit_transform(df)

    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy="median")
    st.session_state["imputer"] = imputer
    df_transform = imputer.fit_transform(df_transform)

    return df_transform

def main():

    experiment_name= setup_page_skeleton()
    option = st.selectbox("Select an option:", ["Build data", "Load data"], index=1)

    if option == "Build data":
        df = build_data(experiment_name)
        if not df.empty:
            df_transform = preprocessing_data(df)
            st.dataframe(pd.DataFrame(df_transform, columns=df.columns))
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
    

if __name__ == "__main__":
    sys.path.insert(1, "./database/")
    main()