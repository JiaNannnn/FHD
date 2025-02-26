"""
Univers Data Management Application

This is the main entry point for the Univers Data Management application.
It provides a Streamlit interface for exporting historical data from IoT devices.
"""
import streamlit as st
import asyncio
from datetime import datetime
import time
import traceback
from pages.export_historical_data import HistoricalDataExporter
from config import load_config, DEFAULT_CONFIGS, validate_config

def main():
    """
    Main function for the Univers Data Management application.
    
    This function sets up the Streamlit UI and handles user interactions.
    """
    st.title("Univers Data Management")
    
    module = st.sidebar.selectbox(
        "Select Module",
        ["Historical Data Export", "Future Module 1", "Future Module 2"]
    )
    
    if module == "Historical Data Export":
        handle_historical_data_export()

def handle_historical_data_export():
    """
    Handle the Historical Data Export module.
    
    This function sets up the UI for the Historical Data Export module
    and processes user inputs.
    """
    exporter = HistoricalDataExporter()
    
    # Project selection
    project_options = list(DEFAULT_CONFIGS.keys()) + ["Custom"]
    selected_project = st.selectbox("Select Project", project_options)

    if selected_project == "Custom":
        access_key = st.text_input("Access Key")
        secret_key = st.text_input("Secret Key", type="password")
        api_gateway = st.text_input("API Gateway")
        org_id = st.text_input("Organization ID")
        project_name = st.text_input("Project Name")
        
        config = {
            "ACCESS_KEY": access_key,
            "SECRET_KEY": secret_key,
            "API_GATEWAY": api_gateway,
            "ORG_ID": org_id,
            "PROJECT_NAME": project_name
        }
    else:
        config = load_config(selected_project)
    
    # Fetch models button
    if st.button("Fetch Models"):
        # Validate configuration
        is_valid, error_message = validate_config(config)
        if not is_valid:
            st.error(error_message)
            return
        
        # Configure exporter with selected project
        exporter.configure(config)
        
        # Fetch models
        with st.spinner("Fetching models..."):
            try:
                models = exporter.search_models()
                
                if not models:
                    st.warning("No models found. Please check your credentials and try again.")
                    return
                    
                # Store models in session state for later use
                st.session_state.models = models
                st.session_state.config = config
                st.success(f"Found {len(models)} models")
            except Exception as e:
                st.error(f"Error fetching models: {str(e)}")
                st.error(f"Please check your credentials and try again.")
                st.expander("Error details").write(traceback.format_exc())
                return
    
    # Model selection (only show if models have been fetched)
    if 'models' in st.session_state and 'config' in st.session_state:
        st.subheader("Select Models")
        
        # Add "Select All" checkbox
        select_all = st.checkbox("Select All Models")
        
        # Create a checkbox for each model
        selected_models = []
        
        # If select_all is checked, select all models by default
        default_checked = select_all
        
        for model in st.session_state.models:
            model_id = model.get("modelId", "Unknown")
            is_selected = st.checkbox(f"Model: {model_id}", value=default_checked)
            if is_selected:
                selected_models.append(model)
        
        # Date selection
        st.subheader("Select Date Range")
        start_date = st.date_input("Start Date", datetime.now().replace(day=1)).strftime("%Y-%m-%d") + " 00:00:00"
        end_date = st.date_input("End Date", datetime.now()).strftime("%Y-%m-%d") + " 23:59:59"
        
        # Data interval selection
        st.subheader("Data Settings")
        interval_options = {
            "1 minute": 1,
            "5 minutes": 5,
            "10 minutes": 10,
            "15 minutes": 15,
            "30 minutes": 30,
            "60 minutes": 60
        }
        interval_selection = st.selectbox(
            "Data Interval",
            options=list(interval_options.keys()),
            index=1  # Default to 5 minutes
        )
        interval_minutes = interval_options[interval_selection]

        # Run button
        if st.button("Run Export"):
            if not selected_models:
                st.error("Please select at least one model")
                return
                
            start_time = time.time()
            
            # Configure exporter with stored config
            exporter.configure(st.session_state.config)
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Pass selected models and interval to the process_historical_data method
                asyncio.run(exporter.process_historical_data(
                    start_date, 
                    end_date, 
                    progress_bar, 
                    status_text, 
                    selected_models,
                    interval_minutes
                ))
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                st.success(f"Process completed in {elapsed_time:.2f} seconds!")
            except Exception as e:
                st.error(f"Error during export: {str(e)}")
                st.expander("Error details").write(traceback.format_exc())

if __name__ == "__main__":
    main() 