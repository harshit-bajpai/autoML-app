import streamlit as st

def setup_page_skeleton():

    st.set_page_config(page_title="Download Config", page_icon="📥", layout="wide")
    st.markdown("# Download Configuration")
    return

def main():

    setup_page_skeleton()
    return

if __name__ == "__main__":
    main()