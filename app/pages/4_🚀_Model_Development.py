import logging
import sys
import traceback

import pandas as pd
import streamlit as st

PAGE_NAME = "4_Model_Development"

def setup_page_skeleton():
    try:
        st.set_page_config(page_title="Model Development", page_icon="🚀", layout="wide")
        st.markdown("# Model Training & Evaluation")
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.")
        logging.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.\
            \n{err}\n{traceback.format_exc()}")

def model_train_st(X_train, y_train, X_test, y_test, model_name):
    from modelDev.modelTrain import ModelTrain
    model_train_obj = ModelTrain(X_train, y_train, X_test, y_test, model_name)
    model_train_obj.train()
    model_train_obj.evaluate()
    return model_train_obj

def main():
    try:
        setup_page_skeleton()
        if "X_train" in st.session_state:
            model_name = st.selectbox("Select a model:", ["Linear Regression", "AutoML Routine"])
            st.session_state["model_name"] = model_name
            if st.button("▶️ Train and Evaluate Model"):
                X_train = pd.DataFrame(st.session_state["X_train"])
                y_train = pd.Series(st.session_state["y_train"])
                X_test = pd.DataFrame(st.session_state["X_test"])
                y_test = pd.Series(st.session_state["y_test"])
                model_train_obj = model_train_st(X_train, y_train, X_test, y_test, model_name)
                st.session_state["model_params"] = model_train_obj.model_params
                st.text(f"{model_name} model trained and evaluated.")
                st.text(f"Model evaluation metrics \n{model_train_obj.get_metrics()}")
                st.session_state["metrics"] = model_train_obj.get_metrics()
        else:
            exp = RuntimeError("Data not found. Please ensure you have uploaded a dataset.")
            st.exception(exp)
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error in the main method.")
        logging.error(f"{PAGE_NAME} page ran into an error in the main method.\n{err}\n{traceback.format_exc()}")
    

if __name__ == "__main__":
    sys.path.insert(1, "./modelDev/")
    main()
