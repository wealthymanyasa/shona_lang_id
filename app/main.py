from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.language_identification import identify_language
from app.model_publisher import publish_model
from app.huggingface_publisher import publish_dataset

app = FastAPI(title="Language Identification API")

class TextInput(BaseModel):
    text: str

class DatasetPublishRequest(BaseModel):
    hf_token: str
    repo_id: str
    dataset_files: List[str]
    readme_file: Optional[str] = "README.md"

class ModelPublishRequest(BaseModel):
    hf_token: str
    repo_id: str
    model_path: str

@app.get("/")
def read_root():
    return {"message": "Language Identification API", "version": "1.0.0"}

@app.post("/identify/")
def identify_language_endpoint(text_input: TextInput):
    """Identify the language of the given text"""
    result = identify_language(text_input.text)
    return result

@app.post("/publish/dataset/")
def publish_dataset_endpoint(request: DatasetPublishRequest):
    """Publish a dataset to Hugging Face Hub"""
    try:
        publish_dataset(
            hf_token=request.hf_token,
            repo_id=request.repo_id,
            dataset_files=request.dataset_files,
            readme_file=request.readme_file
        )
        return {"message": f"Dataset {request.repo_id} published successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.post("/publish/model/")
def publish_model_endpoint(request: ModelPublishRequest):
    """Publish a model to Hugging Face Hub"""
    try:
        success = publish_model(
            hf_token=request.hf_token,
            repo_id=request.repo_id,
            model_path=request.model_path
        )
        if success:
            return {"message": f"Model {request.repo_id} published successfully"}
        else:
            return {"error": "Failed to publish model"}, 500
    except Exception as e:
        return {"error": str(e)}, 500
