import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="Download Config", page_icon="📥", layout="wide")
    st.markdown("# Download Configuration")
    return

def main():

    setup_page_skeleton()
    with st.container():
        st.write("Download configuration functionality coming soon!")
        st.json({"experiment_name": st.session_state["experiment_name"],
                 "data_details": 
                        {"data_shape": st.session_state["data_shape"],
                         "n_features": st.session_state["n_features"],
                         "n_targets": st.session_state["n_targets"]}})
    return

if __name__ == "__main__":
    main()