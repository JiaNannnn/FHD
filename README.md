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

   **Important**: This application requires the `enos-poseidon` package, not `poseidon`. Make sure you're using the correct package name and version in your requirements.txt file.

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

   **Note**: Ensure that all packages in your requirements.txt file specify versions that actually exist on PyPI. Streamlit Cloud will fail to deploy if it cannot find the exact package versions you've specified.

4. For secure credential management:
   - Use Streamlit's secrets management for API keys
   - Navigate to your app settings in Streamlit Cloud
   - Add your API credentials to the secrets section

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
  - `requirements.txt` - Python dependencies

## Development

### Adding a New Project

To add a new project, update the `DEFAULT_CONFIGS` dictionary in `config.py`.

### Adding a New Feature

1. Create a new file in the `pages/` directory
2. Add the module to the selection list in `main.py`
3. Implement the module's functionality

## Troubleshooting

- **Import Error with Poseidon**: Make sure you're using `enos-poseidon` in your requirements.txt, not `poseidon`
- **Package Version Errors**: Ensure all package versions in requirements.txt actually exist on PyPI. For `enos-poseidon`, available versions include 0.1.5, 0.1.6, 0.1.8, 0.1.9, 0.2.0 (not 0.1.0)
- **API Key Format Issues**: Ensure your API keys contain hyphens and follow the correct format
- **File Download Issues**: When deployed on Streamlit Cloud, use the browser download buttons rather than local file saving
- **Deployment Failures**: Check the deployment logs on Streamlit Cloud for specific error messages. Common issues include:
  - Non-existent package versions
  - Python version compatibility problems
  - Missing dependencies
  - Import errors

## License

[Specify your license here]

## Contact

[Your contact information] 