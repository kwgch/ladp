# LADP Sample Application

A sample application demonstrating the LLM Autonomous Dialogue Protocol (LADP).

## Setup

1.  Clone this repository.
2.  Create a virtual environment: `python -m venv .venv` and activate it.
3.  Install dependencies: `pip install -r requirements.txt` (currently empty)
4.  Create a `config.json` file in the root of the project (`/app/config.json`) by copying `config.example.json` and add your API keys:
    ```bash
    cp config.example.json config.json 
    ```
    Then edit `config.json` with your actual API keys. Alternatively, set environment variables like `OPENAI_API_KEY`.

## Usage

Navigate to the root of the project (`/app/`) and run the application using:

```bash
python -m ladp_app.main "Your discussion theme or question here" 
```
Or, to use a different config file location:
```bash
python -m ladp_app.main "Your theme" --config /path/to/your/config.json
```
