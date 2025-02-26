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

3. Configure your API credentials:
   - Edit `univers_app/config.py` with your API credentials
   - Alternatively, create a `.env` file based on `.env.example`

## Usage

Run the application:
```bash
streamlit run univers_app/main.py
```

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

## License

[Specify your license here]

## Contact

[Your contact information] 