import os
from dotenv import load_dotenv

# Default configurations
DEFAULT_CONFIGS = {
    "Concorde": {
        "ACCESS_KEY": "dfe0cec0-6eed-41ab-af2f-90c97bf0e698",
        "SECRET_KEY": "949aeb70-5383-4506-84f7-efc7a538d390",
        "API_GATEWAY": "https://ag-eu2.envisioniot.com",
        "ORG_ID": "o16779139592841674",
        "PROJECT_NAME": "Concorde"
    },
    "CAG":{
        "ACCESS_KEY": "a19a81ad-3310-4f9b-a84d-2482d6d9a947",
        "SECRET_KEY": "1294a0ea-e074-44be-ae2c-4180ffd68960",
        "API_GATEWAY": "https://apim-sg1.envisioniot.com",
        "ORG_ID": "o17134091232951160",
        "PROJECT_NAME": "CAG"
    },
    "STE1":{
        "ACCESS_KEY": "ea53c714-0262-444f-93cc-f38ed1747744",
        "SECRET_KEY": "262a9809-6fdc-46b2-8fa4-62c0140b0715",
        "API_GATEWAY": "https://ag-eu2.envisioniot.com",
        "ORG_ID": "o16709107221201898",
        "PROJECT_NAME": "STE"
    }
    
    # Add more project configurations as needed
}

def load_config(project_name=None):
    """Load configuration from .env file or use defaults"""
    load_dotenv()
    
    if project_name and project_name in DEFAULT_CONFIGS:
        config = DEFAULT_CONFIGS[project_name]
    else:
        config = {
            "ACCESS_KEY": os.getenv("ACCESS_KEY"),
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "API_GATEWAY": os.getenv("API_GATEWAY"),
            "ORG_ID": os.getenv("ORG_ID"),
            "PROJECT_NAME": os.getenv("PROJECT_NAME")
        }
    
    return config 