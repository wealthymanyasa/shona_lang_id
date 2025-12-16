# Language Services API

This project provides a flexible and scalable FastAPI-based API for a variety of language-related tasks, including language identification, and publishing models and datasets to the Hugging Face Hub.

## Overview

The API is designed to be a central service for your language-processing needs. It's built with a modular structure, making it easy to add new features and evolve the application over time.

### Core Features:

- **Language Identification**: An endpoint to identify the language of a given text.
- **Hugging Face Integration**: Endpoints to publish datasets and models directly to the Hugging Face Hub.
- **Scalable Architecture**: Built with FastAPI and Gunicorn for high performance and production readiness.
- **Easy to Extend**: The modular design allows you to easily add new language-related services.

## Getting Started

### Prerequisites

- Python 3.8+
- An environment variable manager (e.g., `python-dotenv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your Hugging Face API token:
    ```
    HF_TOKEN="your-hugging-face-token"
    ```

### Running the Application

To run the application in a development environment, use the following command:

```bash
uvicorn main:app --reload
```

This will start the development server, and you can access the API at `http://127.0.0.1:8000`.

For a production environment, you can use the provided Gunicorn configuration:

```bash
gunicorn -c gunicorn.py main:app
```

## API Endpoints

Once the application is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

Here's a summary of the available endpoints:

-   **`POST /identify/`**: Identifies the language of a given text.
    -   **Body**: `{"text": "your text here"}`
-   **`POST /publish/dataset/`**: Publishes a dataset to the Hugging Face Hub.
    -   **Body**: `{"repo_id": "your-repo-id", "dataset_files": ["path/to/file1.txt"], "readme_file": "path/to/README.md"}`
-   **`POST /publish/model/`**: Publishes a model to the Hugging Face Hub.
    -   **Body**: `{"repo_id": "your-repo-id", "model_path": "path/to/your/model"}`

## How to Extend the API

The application is designed to be easily extended. To add a new feature:

1.  **Create a new module** in the `app` directory (e.g., `app/summarization.py`).
2.  **Implement your logic** in the new module.
3.  **Add a new endpoint** in `main.py` that uses your new module.

This modular approach keeps the codebase clean and makes it easy to manage as the application grows.

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, please open an issue or submit a pull request.
