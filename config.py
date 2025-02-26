"""
Configuration Module

This module contains configuration settings for different projects.
All configuration is defined directly in this file rather than using environment variables.
"""

# Project configurations
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