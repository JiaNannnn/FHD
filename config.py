"""
Configuration Module

This module contains configuration settings for different projects.
It supports both hardcoded configs (for development) and Streamlit secrets (for deployment).
"""
import streamlit as st
import json
import time
import traceback

# Project configurations - fallback for development
DEFAULT_CONFIGS = {
    "Concorde": {
        "ACCESS_KEY": "dfe0cec0-6eed-41ab-af2f-90c97bf0e698",
        "SECRET_KEY": "949aeb70-5383-4506-84f7-efc7a538d390",
        "API_GATEWAY": "https://ag-eu2.envisioniot.com",
        "ORG_ID": "o16779139592841674",
        "PROJECT_NAME": "Concorde"
    },
    "CAG": {
        "ACCESS_KEY": "a19a81ad-3310-4f9b-a84d-2482d6d9a947",
        "SECRET_KEY": "1294a0ea-e074-44be-ae2c-4180ffd68960",
        "API_GATEWAY": "https://apim-sg1.envisioniot.com",
        "ORG_ID": "o17134091232951160",
        "PROJECT_NAME": "CAG"
    },
    "STE": {
        "ACCESS_KEY": "ea53c714-0262-444f-93cc-f38ed1747744",
        "SECRET_KEY": "262a9809-6fdc-46b2-8fa4-62c0140b0715",
        "API_GATEWAY": "https://ag-eu2.envisioniot.com",
        "ORG_ID": "o16709107221201898",
        "PROJECT_NAME": "STE"
    },
    "OCBC": {
        "ACCESS_KEY": "7335b7cb-af5d-426d-8d40-7731c64d9023",
        "SECRET_KEY": "3b31f52e-d384-4ba7-8fea-5980efd206b9",
        "API_GATEWAY": "https://apim-sg1.envisioniot.com",
        "ORG_ID": "o16964846601641784",
        "PROJECT_NAME": "OCBC"
    }
    # Add more project configurations as needed
}

# Default configuration to use when no specific project is selected
DEFAULT_CONFIG = {
    "ACCESS_KEY": "default-access-key-replace-me",
    "SECRET_KEY": "default-secret-key-replace-me",
    "API_GATEWAY": "https://api-gateway-url.com",
    "ORG_ID": "o12345678901234567",
    "PROJECT_NAME": "Default"
}

# Store active configuration globally
_ACTIVE_CONFIG = None

def load_config(project_name=None):
    """
    Load configuration for a specific project.
    
    First tries to load from Streamlit secrets, then falls back to hardcoded configs.
    
    Args:
        project_name (str, optional): Name of the project to load configuration for.
            If None or not found, returns the default configuration.
            
    Returns:
        dict: Configuration dictionary with API credentials
    """
    global _ACTIVE_CONFIG
    
    # First try to get from Streamlit secrets if available
    try:
        if hasattr(st, 'secrets') and 'projects' in st.secrets:
            # Check if the specific project is in secrets
            if project_name and project_name in st.secrets['projects']:
                _ACTIVE_CONFIG = st.secrets['projects'][project_name]
                return _ACTIVE_CONFIG
            # If no project specified but we have a default in secrets
            elif 'default' in st.secrets['projects']:
                _ACTIVE_CONFIG = st.secrets['projects']['default']
                return _ACTIVE_CONFIG
    except:
        # If any error occurs with secrets, just continue to fallback method
        pass
    
    # Fallback to hardcoded configs
    if project_name and project_name in DEFAULT_CONFIGS:
        _ACTIVE_CONFIG = DEFAULT_CONFIGS[project_name]
        return _ACTIVE_CONFIG
    else:
        _ACTIVE_CONFIG = DEFAULT_CONFIG
        return _ACTIVE_CONFIG

def validate_config(config):
    """
    Validate configuration parameters.
    
    Args:
        config (dict): Configuration dictionary with API credentials
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if configuration is valid, False otherwise
            - error_message (str or None): Error message if configuration is invalid, None otherwise
    """
    import streamlit as st
    
    # Debug output
    if st:
        with st.expander("Configuration Debug"):
            st.write("Validating configuration...")
            # Show non-sensitive parts of config
            st.write(f"API Gateway: {config.get('API_GATEWAY', 'Not provided')}")
            st.write(f"Org ID: {config.get('ORG_ID', 'Not provided')}")
            st.write(f"Project Name: {config.get('PROJECT_NAME', 'Not provided')}")
            
            # Show masked keys
            if 'ACCESS_KEY' in config and config['ACCESS_KEY']:
                access_key = config['ACCESS_KEY']
                st.write(f"Access Key (masked): {access_key[:4]}...{access_key[-4:]}")
                st.write(f"Access Key length: {len(access_key)}")
                st.write(f"Access Key contains hyphens: {'-' in access_key}")
            else:
                st.write("Access Key: Not provided")
                
            if 'SECRET_KEY' in config and config['SECRET_KEY']:
                secret_key = config['SECRET_KEY']
                st.write(f"Secret Key (masked): {secret_key[:4]}...{secret_key[-4:]}")
                st.write(f"Secret Key length: {len(secret_key)}")
                st.write(f"Secret Key contains hyphens: {'-' in secret_key}")
            else:
                st.write("Secret Key: Not provided")
    
    # Check for required fields
    required_fields = ["ACCESS_KEY", "SECRET_KEY", "API_GATEWAY", "ORG_ID", "PROJECT_NAME"]
    for field in required_fields:
        if not config.get(field):
            return False, f"Missing required configuration: {field}"
    
    # Skip hyphen validation when in development mode with special flag 
    if config.get("_DEV_MODE_SKIP_VALIDATION", False):
        return True, None
    
    # In Streamlit Cloud, temporarily disable strict validation while we debug
    if st and hasattr(st, 'secrets') and 'projects' in st.secrets:
        # Relaxed validation for Streamlit Cloud deployment
        return True, None
        
    # Validate key format
    access_key = config["ACCESS_KEY"]
    secret_key = config["SECRET_KEY"]
    
    # Check if keys contain hyphens, which is required by poseidon
    if "-" not in access_key:
        return False, "Invalid ACCESS_KEY format. Key should contain hyphens (e.g., 'xxx-yyy-zzz')."
    
    if "-" not in secret_key:
        return False, "Invalid SECRET_KEY format. Key should contain hyphens (e.g., 'xxx-yyy-zzz')."
    
    # Ensure the key has at least 2 parts when split by hyphen
    if len(access_key.split("-")) < 2:
        return False, "Invalid ACCESS_KEY format. Key must have at least two parts separated by hyphens."
    
    if len(secret_key.split("-")) < 2:
        return False, "Invalid SECRET_KEY format. Key must have at least two parts separated by hyphens."
    
    return True, None

def make_api_call(url, data=None, config=None):
    """
    Make an API call using the poseidon library with centralized credential handling.
    
    Args:
        url (str): API endpoint URL
        data (dict, optional): Request data. Defaults to None.
        config (dict, optional): Configuration override. If None, uses active config.
        
    Returns:
        dict: API response
        
    Raises:
        Exception: If API call fails
    """
    from vendor.poseidon import poseidon
    
    # Use provided config or fall back to active config
    cfg = config or _ACTIVE_CONFIG
    if not cfg:
        raise ValueError("No active configuration. Call load_config() first.")
    
    # Validate config
    is_valid, error_message = validate_config(cfg)
    if not is_valid:
        raise ValueError(f"Invalid configuration: {error_message}")
    
    try:
        # Debug - log API call
        print(f"Attempting API call to {url}")
        print(f"Request data: {json.dumps(data) if data else None}")
        
        # Make API call
        response = poseidon.urlopen(
            cfg["ACCESS_KEY"], 
            cfg["SECRET_KEY"], 
            url, 
            data
        )
        
        # Debug - log success
        print(f"API call successful. Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
        return response
        
    except Exception as e:
        # Debug - log error
        print(f"API call failed with error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'response'):
            print(f"Response from server: {e.response}")
        
        # Re-raise exception
        raise

async def make_async_api_call(url, data=None, config=None):
    """
    Make an asynchronous API call using the poseidon library with centralized credential handling.
    
    Args:
        url (str): API endpoint URL
        data (dict, optional): Request data. Defaults to None.
        config (dict, optional): Configuration override. If None, uses active config.
        
    Returns:
        dict: API response
        
    Raises:
        Exception: If API call fails
    """
    from vendor.poseidon import poseidon
    
    # Use provided config or fall back to active config
    cfg = config or _ACTIVE_CONFIG
    if not cfg:
        raise ValueError("No active configuration. Call load_config() first.")
    
    # Validate config
    is_valid, error_message = validate_config(cfg)
    if not is_valid:
        raise ValueError(f"Invalid configuration: {error_message}")
    
    try:
        # Make API call
        return await poseidon.a_urlopen(
            cfg["ACCESS_KEY"], 
            cfg["SECRET_KEY"], 
            url, 
            data
        )
        
    except Exception as e:
        # Re-raise exception
        raise 