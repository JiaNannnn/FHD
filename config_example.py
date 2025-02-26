"""
Example Configuration Module

This is an example of how to configure the application using environment variables
instead of hardcoded credentials for better security.

To use this configuration:
1. Rename this file to config.py
2. Set up environment variables or a .env file with your credentials
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Project configurations using environment variables
DEFAULT_CONFIGS = {
    "Concorde": {
        "ACCESS_KEY": os.getenv("CONCORDE_ACCESS_KEY"),
        "SECRET_KEY": os.getenv("CONCORDE_SECRET_KEY"),
        "API_GATEWAY": os.getenv("CONCORDE_API_GATEWAY", "https://ag-eu2.envisioniot.com"),
        "ORG_ID": os.getenv("CONCORDE_ORG_ID"),
        "PROJECT_NAME": "Concorde"
    },
    "CAG": {
        "ACCESS_KEY": os.getenv("CAG_ACCESS_KEY"),
        "SECRET_KEY": os.getenv("CAG_SECRET_KEY"),
        "API_GATEWAY": os.getenv("CAG_API_GATEWAY", "https://apim-sg1.envisioniot.com"),
        "ORG_ID": os.getenv("CAG_ORG_ID"),
        "PROJECT_NAME": "CAG"
    },
    "STE": {
        "ACCESS_KEY": os.getenv("STE_ACCESS_KEY"),
        "SECRET_KEY": os.getenv("STE_SECRET_KEY"),
        "API_GATEWAY": os.getenv("STE_API_GATEWAY", "https://ag-eu2.envisioniot.com"),
        "ORG_ID": os.getenv("STE_ORG_ID"),
        "PROJECT_NAME": "STE"
    },
    "OCBC": {
        "ACCESS_KEY": os.getenv("OCBC_ACCESS_KEY"),
        "SECRET_KEY": os.getenv("OCBC_SECRET_KEY"),
        "API_GATEWAY": os.getenv("OCBC_API_GATEWAY", "https://apim-sg1.envisioniot.com"),
        "ORG_ID": os.getenv("OCBC_ORG_ID"),
        "PROJECT_NAME": "OCBC"
    }
    # Add more project configurations as needed
}

# Default configuration to use when no specific project is selected
DEFAULT_CONFIG = {
    "ACCESS_KEY": os.getenv("DEFAULT_ACCESS_KEY"),
    "SECRET_KEY": os.getenv("DEFAULT_SECRET_KEY"),
    "API_GATEWAY": os.getenv("DEFAULT_API_GATEWAY", "https://api-gateway-url.com"),
    "ORG_ID": os.getenv("DEFAULT_ORG_ID"),
    "PROJECT_NAME": os.getenv("DEFAULT_PROJECT_NAME", "Default")
}

def load_config(project_name=None):
    """
    Load configuration for a specific project.
    
    Args:
        project_name (str, optional): Name of the project to load configuration for.
            If None or not found, returns the default configuration.
            
    Returns:
        dict: Configuration dictionary with API credentials
    """
    if project_name and project_name in DEFAULT_CONFIGS:
        return DEFAULT_CONFIGS[project_name]
    else:
        return DEFAULT_CONFIG

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
    # Check for required fields
    required_fields = ["ACCESS_KEY", "SECRET_KEY", "API_GATEWAY", "ORG_ID", "PROJECT_NAME"]
    for field in required_fields:
        if not config.get(field):
            return False, f"Missing required configuration: {field}"
    
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