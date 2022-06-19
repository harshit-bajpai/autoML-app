import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="Download Config", page_icon="📥", layout="wide")
    st.markdown("# Download Configuration")
    return

def create_json_config():
    config = {"run_info": 
                {"experiment_name": st.session_state["experiment_name"],
                    "runtime_start": st.session_state["runtime_start"]},
            "data_info": 
                {"data_shape": st.session_state["data_shape"],
                    "n_features": st.session_state["n_features"],
                    "n_targets": st.session_state["n_targets"],
                    "preprocessing_info":
                        {"scaler": st.session_state["scaler"],
                        "imputer" : st.session_state["imputer"],
                        "train_test_split_ratio" : ""}},
            "model_train_info":
                {"model_type": "",
                    "model_name": "",
                    "model_params": {},
                    "metrics": {}},
            "model_eval_info":
                {"metrics": {}}
            }
    return config

def main():

    setup_page_skeleton()
    with st.container():
        st.write("Download configuration functionality coming soon!")
        st.json(create_json_config())
    return

if __name__ == "__main__":
    main()