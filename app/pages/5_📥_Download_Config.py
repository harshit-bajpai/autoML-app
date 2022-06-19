import time
import streamlit as st

def setup_page_skeleton():
    st.set_page_config(page_title="Download Config", page_icon="📥", layout="wide")
    st.markdown("# Download Configuration")
    return

def create_json_config() -> dict:
    try:
        config = {"run_info": 
                {"experiment_name": st.session_state["experiment_name"] if "experiment_name" in st.session_state else "",
                    "runtime_start": st.session_state["runtime_start"] if "runtime_start" in st.session_state else ""},
            "data_info": 
                {"data_generator": st.session_state["data_generator"] if "data_generator" in st.session_state else "",
                    "data_shape": st.session_state["data_shape"] if "data_shape" in st.session_state else "",
                    "n_features": st.session_state["n_features"] if "n_features" in st.session_state else "",
                    "n_targets": st.session_state["n_targets"] if "n_targets" in st.session_state else ""},
                    "id_col": st.session_state["id_col"] if "id_col" in st.session_state else "",
                    "timestamp_col": st.session_state["timestamp_col"] if "timestamp_col" in st.session_state else "",
                    "preprocessing_info":
                        {"scaler": st.session_state["scaler"] if "scaler" in st.session_state else "",
                        "imputer" : st.session_state["imputer"] if "imputer" in st.session_state else "",
                        "train_test_split_ratio" : ""},
            "model_train_info":
                {"model_type": "",
                    "model_name": "",
                    "model_params": {},
                    "metrics": {}},
            "model_eval_info":
                {"metrics": {}}
            }
        return config
    except Exception as err:
        st.error(f"Ran into an error while creating json config")

def main():
    try:
        setup_page_skeleton()
        with st.container():
            st.json(create_json_config())
        st.write("Download config functionality is not yet implemented")
    except Exception as err:
        st.error(f"Ran into an error while loading page 5")

if __name__ == "__main__":
    main()