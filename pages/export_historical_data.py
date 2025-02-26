"""
Historical Data Exporter Module

This module provides functionality to export historical data from IoT devices.
It handles searching for models, device assets, and retrieving/transforming historical data.
"""
try:
    # Try importing from enos-poseidon package first
    from poseidon import poseidon
except ImportError:
    try:
        # Try alternative import pattern for enos-poseidon
        import poseidon
    except ImportError:
        # If all imports fail, create a mock for development/testing
        class MockPoseidon:
            @staticmethod
            def urlopen(access_key, secret_key, url, data):
                print(f"MOCK API CALL: {url}")
                return {"data": {"items": []}}
                
            @staticmethod
            async def a_urlopen(access_key, secret_key, url, data):
                print(f"MOCK ASYNC API CALL: {url}")
                return {"data": {"items": []}}
        
        poseidon = MockPoseidon()
        print("Using mock poseidon module (API calls will not work)")

import json
import os
import pandas as pd
from datetime import datetime
import asyncio
import pytz
import streamlit as st
from utils.time_utils import current_milli_time, round_to_nearest_interval, split_into_daily_intervals

class HistoricalDataExporter:
    """
    A class for exporting historical data from IoT devices.
    
    This class provides methods to search for models and device assets,
    retrieve historical data, and transform it into CSV format.
    """
    
    def __init__(self):
        """Initialize the HistoricalDataExporter with empty credentials."""
        self.accessKey = None
        self.secretKey = None
        self.api_gateway = None
        self.orgId = None
        self.projectName = None

    def configure(self, config):
        """
        Configure the exporter with the provided credentials.
        
        Args:
            config (dict): Configuration dictionary containing API credentials
        """
        self.accessKey = config["ACCESS_KEY"]
        self.secretKey = config["SECRET_KEY"]
        self.api_gateway = config["API_GATEWAY"]
        self.orgId = config["ORG_ID"]
        self.projectName = config["PROJECT_NAME"]
        
    def _safe_urlopen(self, url, data):
        """
        Wrapper around poseidon.urlopen with error handling.
        
        Args:
            url (str): URL to open
            data (dict): Data to send
            
        Returns:
            dict: Response from the API
            
        Raises:
            Exception: If the API call fails
        """
        try:
            return poseidon.urlopen(self.accessKey, self.secretKey, url, data)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            raise

    async def _safe_a_urlopen(self, url, data):
        """
        Wrapper around poseidon.a_urlopen with error handling.
        
        Args:
            url (str): URL to open
            data (dict): Data to send
            
        Returns:
            dict: Response from the API
            
        Raises:
            Exception: If the API call fails
        """
        try:
            return await poseidon.a_urlopen(self.accessKey, self.secretKey, url, data)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            raise

    def search_models(self):
        """
        Search for models in the system.
        
        Returns:
            list: List of models with their identifiers
        """
        url = f'{self.api_gateway}/model-service/v2.1/thing-models?action=search&orgId={self.orgId}'
        data = {
            "projection": ["modelId", "modelIdPath", "measurepoints"],
            "pagination": {
                "pageNo": 1,
                "pageSize": 500
            }
        }
        req = self._safe_urlopen(url, data)
        json_data = req["data"]['items']
        return self._extract_model_and_identifiers(json_data)

    def _extract_model_and_identifiers(self, json_data):
        """
        Extract model IDs and their associated identifiers from API response.
        
        Args:
            json_data (list): List of model data from API
            
        Returns:
            list: List of dictionaries containing modelId and identifiers
        """
        extracted_data = []
        for obj in json_data:
            identifiers = []
            for mp in obj.get("measurepoints", {}).values():
                identifiers.append(mp.get("identifier"))
            extracted_data.append({"modelId": obj.get("modelId", ""), "identifiers": identifiers})
        return extracted_data

    def search_device_assets(self, device_name_pattern="OC-004"):
        """
        Search for device assets in the system.
        
        Args:
            device_name_pattern (str): Pattern to match device names
            
        Returns:
            dict: Device assets data
        """
        url = f"{self.api_gateway}/connect-service/v2.1/devices?action=search&orgId={self.orgId}"
        data = {
            #"expression": f"deviceName.default like '{device_name_pattern}'",
            "pagination": {
                "pageNo": 1,
                "pageSize": 1000
            }
        }
        req = self._safe_urlopen(url, data)
        return req["data"]

    async def get_historical_data(self, asset_id, identifiers_str, start_time, end_time, interval=300):
        """
        Get historical data for a specific asset and time range.
        
        Args:
            asset_id (str): Asset ID
            identifiers_str (str): Comma-separated identifiers
            start_time (datetime): Start time
            end_time (datetime): End time
            interval (int, optional): Data interval in seconds. Default is 300 (5 minutes).
            
        Returns:
            dict: Historical data response
        """
        url = f'{self.api_gateway}/tsdb-service/v2.1/raw?orgId={self.orgId}'
        data = {
            "pointIds": identifiers_str,
            "assetIds": asset_id,
            "startTime": start_time.isoformat(),
            "endTime": end_time.isoformat(),
            "interval": interval,
            "pageSize": 6000
        }
        req = await self._safe_a_urlopen(url, data)
        return req

    def transform_json_list(self, asset_name, nested_json_list, asset_id, interval_minutes=5):
        """
        Transform JSON data into CSV format.
        
        Args:
            asset_name (str): Asset name for file naming
            nested_json_list (list): List of JSON data
            asset_id (str): Asset ID
            interval_minutes (int, optional): Data interval in minutes for rounding timestamps.
                Default is 5.
                
        Returns:
            tuple: (csv_data, filename) - The CSV data as a string and the suggested filename
        """
        transformed_data = []
        if len(nested_json_list) == 0 or all(len(row) == 0 for row in nested_json_list):
            return None, None

        for i in range(len(nested_json_list)):
            for nested_json in nested_json_list[i]:
                if isinstance(nested_json, dict):
                    point_id = next((key for key in nested_json if key not in ['assetId', 'timestamp', 'localtime']), None)
                    point_value = nested_json.get(point_id) if point_id else None
                    
                    dt = datetime.strptime(nested_json.get('localtime'), "%Y-%m-%d %H:%M:%S")
                    rounded_dt = round_to_nearest_interval(dt, interval_minutes)
                    
                    transformed_entry = {
                        'pointId': point_id,
                        'pointValue': point_value,
                        'assetId': nested_json.get('assetId'),
                        'timestamp': nested_json.get('timestamp'),
                        'localtime': rounded_dt.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    transformed_data.append(transformed_entry)

        if not transformed_data:
            return None, None
            
        df = pd.DataFrame(transformed_data)
        df_pivoted = df.pivot_table(index='localtime', columns='pointId', values='pointValue', aggfunc='first').reset_index()
        
        # Generate CSV data
        csv_data = df_pivoted.to_csv(index=False)
        
        # Create a directory for saving files locally if needed
        if not os.path.exists(self.projectName):
            os.makedirs(self.projectName)
        
        # Also save a local copy
        output_file = f'{self.projectName}/{asset_name}-{asset_id}.csv'
        df_pivoted.to_csv(output_file, index=False)
        
        # Return CSV data and filename for download
        filename = f"{asset_name}-{asset_id}.csv"
        return csv_data, filename

    async def process_historical_data(self, start_date, end_date, progress_bar, status_text, selected_models=None, interval_minutes=5):
        """
        Process historical data for all assets in the given time range.
        
        Args:
            start_date (str): Start date in format 'YYYY-MM-DD HH:MM:SS'
            end_date (str): End date in format 'YYYY-MM-DD HH:MM:SS'
            progress_bar (streamlit.ProgressBar): Progress bar for UI feedback
            status_text (streamlit.empty): Text element for status updates
            selected_models (list, optional): List of selected models to process.
                If None, all models will be processed.
            interval_minutes (int, optional): Data interval in minutes. 
                Supported values: 1, 5, 10, 15, 30, 60. Default is 5.
        """
        # Convert interval from minutes to seconds
        interval_seconds = interval_minutes * 60
        
        # List to store downloadable files
        download_files = []
        
        assets = self.search_device_assets()
        
        # Define model_list before using it
        if selected_models is None:
            model_list = self.search_models()
        else:
            model_list = selected_models
            
        status_text.text(f"Processing {len(model_list)} selected models")
        
        # Filter assets based on selected models
        asset_with_mps = []
        asset_and_name = []
        
        for asset in assets:
            asset_model_id = asset["modelId"]
            
            for model in model_list:
                model_id = model["modelId"]
                if model_id == asset_model_id:
                    asset_and_name.append(f"{asset['assetId']}:{asset['deviceName']['defaultValue']}")
                    asset_with_mps.append(asset['assetId'])
                    asset_with_mps.append(model["identifiers"])

        if not asset_with_mps:
            status_text.text("No matching assets found for the selected models")
            st.warning("No matching assets were found for the selected models. Please select different models or check your device configurations.")
            return

        total_assets = len(range(0, len(asset_with_mps), 2))
        for idx, i in enumerate(range(0, len(asset_with_mps), 2)):
            status_text.text(f"Processing asset {idx + 1} of {total_assets}")
            progress_bar.progress((idx + 1) / total_assets)
            
            for item in asset_and_name:
                asset_id, asset_name = item.split(":")
                if asset_id == asset_with_mps[i]:
                    identifiers = asset_with_mps[i + 1]
                    identifiers_str = ",".join(identifiers)
                    
                    timezone = pytz.timezone('Asia/Singapore')
                    start_datetime = timezone.localize(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
                    end_datetime = timezone.localize(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
                    
                    tasks = []
                    for start_time, end_time in split_into_daily_intervals(start_datetime.isoformat(), end_datetime.isoformat()):
                        tasks.append(self.get_historical_data(asset_id, identifiers_str, start_time, end_time, interval_seconds))
                    
                    status_text.text(f"Fetching historical data for {asset_name}...")
                    responses = await asyncio.gather(*tasks)
                    
                    result = []
                    status_text.text(f"Transforming data for {asset_name}...")
                    for his_data in responses:
                        if his_data is not None and his_data.get("data") is not None:
                            result.append(his_data["data"]["items"])
                    
                    csv_data, filename = self.transform_json_list(asset_name, result, asset_id, interval_minutes)
                    if csv_data and filename:
                        download_files.append((csv_data, filename, asset_name))
        
        # Display file download options
        if download_files:
            # Primary option: Direct browser downloads
            st.subheader("Download Files")
            
            # Show a neat table with download buttons
            for i, (csv_data, filename, asset_name) in enumerate(download_files):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{asset_name}** - {filename}")
                with col2:
                    st.download_button(
                        label="Download",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        key=f"download_{filename}"
                    )
            
            # Add option to download all files as ZIP
            if len(download_files) > 1:
                st.markdown("---")
                import io
                import zipfile
                
                # Create ZIP file in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for csv_data, filename, _ in download_files:
                        zip_file.writestr(filename, csv_data)
                
                # Offer ZIP download button
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Download all files in a single ZIP archive**")
                with col2:
                    st.download_button(
                        label="Download ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"{self.projectName}_export.zip",
                        mime="application/zip"
                    )
            
            # Secondary option: Local file system (in expander)
            with st.expander("Save to Local Directory (Advanced)"):
                st.warning("This option is only available when running Streamlit locally, not on Streamlit Cloud.")
                
                # Simple path input
                save_dir = st.text_input(
                    "Directory path:", 
                    value=self.projectName,
                    help="Enter a path like 'C:/Downloads/data' (Windows) or '/home/user/data' (Linux/Mac)"
                )
                
                # Create directory if needed
                if st.button("Save All Files"):
                    if not os.path.exists(save_dir):
                        try:
                            os.makedirs(save_dir)
                            st.success(f"Created directory: {save_dir}")
                        except Exception as e:
                            st.error(f"Error creating directory: {str(e)}")
                            st.stop()
                    
                    # Save all files
                    with st.spinner("Saving files..."):
                        saved_files = []
                        for csv_data, filename, _ in download_files:
                            try:
                                file_path = os.path.join(save_dir, filename)
                                with open(file_path, 'w') as f:
                                    f.write(csv_data)
                                saved_files.append(file_path)
                            except Exception as e:
                                st.error(f"Error saving {filename}: {str(e)}")
                        
                        if saved_files:
                            st.success(f"✅ Saved {len(saved_files)} files to {save_dir}")
                            with st.expander("View saved file paths"):
                                for path in saved_files:
                                    st.code(path)
        
        return download_files

# For backwards compatibility with any code that might import ExportHistoricalData
class ExportHistoricalData(HistoricalDataExporter):
    """
    Alias for HistoricalDataExporter for backwards compatibility.
    
    This class inherits from HistoricalDataExporter and overrides the __init__ method
    to match the original ExportHistoricalData signature.
    """
    
    def __init__(self, projectName):
        """
        Initialize the ExportHistoricalData with a project name.
        
        Args:
            projectName (str): Name of the project for file organization
        """
        super().__init__()
        self.projectName = projectName 