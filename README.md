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

- **API Key Format Issues**: Ensure your API keys contain hyphens and follow the correct format
- **File Download Issues**: When deployed on Streamlit Cloud, use the browser download buttons rather than local file saving
- **Deployment Failures**: Check the deployment logs on Streamlit Cloud for specific error messages. Common issues include:
  - Python version compatibility problems
  - Missing dependencies
  - Import errors

## License

[Specify your license here]

## Contact

[Your contact information] 