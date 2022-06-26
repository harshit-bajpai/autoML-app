import json
import logging
import os
import time
import traceback
from logging.handlers import TimedRotatingFileHandler

import streamlit as st

PAGE_NAME = "1_Home"

def setup_logging(req_id: str, log_level: str) -> None:
    """
    Set up the logging for the application with TimedRotatingFileHandler
    """

    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    filename = "st_app.log"
    filepath = f"./logs/{filename}"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = TimedRotatingFileHandler(filepath,
                                    when="midnight")

    format = f'%(levelname)s %(asctime)s {req_id} %(message)s '
    logging.basicConfig(format=format,
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=f"{log_level}",
                        handlers=[handler])


    logging.info(f"Logging started for {req_id} experiment")

def page_skeleton() -> None:
    try:
        st.set_page_config(page_title="autoML", page_icon="👋", layout="wide")

        with st.spinner("Loading App Configuration..."):
            load_app_config()

        st.write("# AutoML Application👋")

        st.sidebar.success("Welcome to the AutoML application! \
                    Please go through the options in the sidebar sequently.")
                    
        experiment_name = st.text_input("Enter experiment name:", "", 16)

        if experiment_name != "":
            setup_logging(experiment_name, st.session_state["config"]["log_level"])
            st.session_state["experiment_name"] = experiment_name
            st.session_state["runtime_start"] = time.strftime('%Y-%m-%d %H:%M:%S', 
                time.localtime(time.time()))        
        else:
            exp = KeyError("Experiment name is empty")
            st.exception(exp)
        
        st.markdown(
                """
                ---
                
                ### Auto ML Application version : 0.1.0 
                > Minimum Viable Product


                Supported Features:
                - [x] ETL
                - [x] Model Training
                - [x] Model Evaluation
                - [x] Export Configuration

                """
                )
    except Exception as err:
        st.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.")
        logging.error(f"{PAGE_NAME} page ran into an error while setting up skeleton.\
            \n{err}\n{traceback.format_exc()}")

def load_app_config() -> None:
    with open("./app/app_config.json", "r") as f:
        config = json.load(f)
    st.session_state["config"] = config

def main():
    page_skeleton()

if __name__ == "__main__":
    main()
