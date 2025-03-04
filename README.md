# Univers Data Management Application

A Streamlit-based application for managing and exporting historical data from IoT devices using Poseidon API.

## ⚠️ Security Warning

**IMPORTANT**: This repository contains sample configuration with API credentials in `config.py`. Before deploying or sharing this code:

1. Move all credentials to environment variables or a secure secrets manager
2. Update `config.py` to use environment variables instead of hardcoded values
3. Consider using a `.env` file locally (added to `.gitignore`)

## Features

- Historical data export from IoT devices to CSV files
- Multiple project configuration support
- Model selection with filtering capabilities
- Flexible data interval selection (1, 5, 10, 15, 30, 60 minutes)
- Progress tracking with visual feedback

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/univers-app.git
   cd univers-app
   ```

2. Install dependencies:
   ```bash
   pip install -r univers_app/requirements.txt
   ```

   **Note**: This application uses an embedded version of the poseidon library (included in the `vendor` directory), so you don't need to install `enos-poseidon` separately.

3. Configure your API credentials:
   - Edit `univers_app/config.py` with your API credentials
   - Alternatively, create a `.env` file based on `.env.example`
   - **API Key Format**: Ensure your API keys contain hyphens (format: xxxx-xxxx-xxxx-xxxx)

## Usage

Run the application locally:
```bash
streamlit run univers_app/main.py
```

## Deployment on Streamlit Cloud

This application is designed to be deployed on Streamlit Cloud:

1. Push your code to a GitHub repository:
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. Deploy on Streamlit Cloud:
   - Go to [Streamlit Cloud](https://share.streamlit.io/)
   - Connect your GitHub account
   - Select this repository
   - Set the main file path to: `univers_app/main.py`

3. Streamlit Cloud automatically:
   - Detects and installs dependencies from `requirements.txt`
   - Sets up a virtual environment for your application
   - Serves your application with HTTPS

   **Note**: The application uses the embedded poseidon library from the `vendor` directory, eliminating any dependency issues with the external `enos-poseidon` package.

4. For secure credential management:
   - Use Streamlit's secrets management for API keys
   - Navigate to your app settings in Streamlit Cloud
   - Add your API credentials to the secrets section

### Critical: Setting Up Secrets in Streamlit Cloud

If you're experiencing the "No models found" error on Streamlit Cloud, this is most likely due to missing or incorrectly formatted API credentials. Follow these steps to fix it:

1. **Format Your API Keys**: Ensure your API keys contain hyphens (format: xxxx-xxxx-xxxx-xxxx)
2. **Add Secrets to Streamlit Cloud**:
   - Go to your app dashboard in Streamlit Cloud
   - Click on "Settings" → "Secrets"
   - Copy and paste the following template, replacing with your actual API keys:

```toml
# Each project should be under the [projects] section
[projects]

# Default project that will be used if no specific project is selected
[projects.default]
ACCESS_KEY = "your-access-key-with-hyphens"
SECRET_KEY = "your-secret-key-with-hyphens"
API_GATEWAY = "https://ag-eu2.envisioniot.com"
ORG_ID = "o16779139592841674"
PROJECT_NAME = "Default Project"

# Add other projects as needed
[projects.ProjectName]
ACCESS_KEY = "project-specific-access-key"
SECRET_KEY = "project-specific-secret-key"
API_GATEWAY = "https://api-gateway-url.com"
ORG_ID = "org-id-value"
PROJECT_NAME = "Project Name"
```

3. **Save and Restart**: Click "Save" in the secrets manager, then restart your Streamlit app

A sample secrets template file is available at `.streamlit/secrets_example.toml` for reference.

## Browser Download vs. Local File Saving

- When deployed on Streamlit Cloud, use the browser download functionality to get your exported files
- Local file saving is only available when running the application locally on your machine

## Project Structure

- `univers_app/` - Main application directory
  - `main.py` - Application entry point
  - `config.py` - Configuration management
  - `pages/` - Application modules
    - `export_historical_data.py` - Historical data export functionality
  - `utils/` - Utility functions
    - `time_utils.py` - Time-related utility functions
  - `vendor/` - Embedded third-party libraries
    - `poseidon/` - Custom poseidon library with both sync and async API functionality
  - `requirements.txt` - Python dependencies
  - `.streamlit/` - Streamlit configuration
     - `secrets_example.toml` - Example secrets file for Streamlit Cloud deployment

## Development

### Adding a New Project

To add a new project, update the `DEFAULT_CONFIGS` dictionary in `config.py`.

### Adding a New Feature

1. Create a new file in the `pages/` directory
2. Add the module to the selection list in `main.py`
3. Implement the module's functionality

### Updating the Embedded Poseidon Library

If you need to update the poseidon library functionality:

1. Modify the files in the `vendor/poseidon/` directory
2. Test your changes locally
3. Commit and push to deploy to Streamlit Cloud

## Troubleshooting

### "No models found" Error

This error typically occurs when:

1. **API Credentials**: Your API keys are missing or incorrectly formatted
   - Solution: Add properly formatted API keys with hyphens to Streamlit Cloud secrets

2. **Connection Issues**: The application cannot connect to the API
   - Solution: Check if the API Gateway URL is correct and accessible

3. **Validation Failures**: The credential validation is failing
   - Solution: Ensure your API keys follow the required format with hyphens

### Other Common Issues

- **File Download Issues**: When deployed on Streamlit Cloud, use the browser download buttons rather than local file saving
- **Deployment Failures**: Check the deployment logs on Streamlit Cloud for specific error messages. Common issues include:
  - Python version compatibility problems
  - Missing dependencies
  - Import errors

## License

[Specify your license here]

## Contact

[Your contact information] 