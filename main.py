from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

from app.huggingface_publisher import publish_dataset
from app.language_identification import identify_language
from app.model_publisher import publish_model

load_dotenv()  # Load environment variables from .env file

app = FastAPI(
    title="Language Services API",
    description="An API for language identification and publishing models and datasets to the Hugging Face Hub.",
    version="1.0.0",
)

# --- Pydantic Models ---

class DatasetPublishRequest(BaseModel):
    repo_id: str = Field(..., example="omanyasa/bantu-lang-id-dataset")
    dataset_files: List[str] = Field(..., example=["data/shona_en_lang_train.txt"])
    readme_file: str = Field("README.md", example="README.md")

class ModelPublishRequest(BaseModel):
    repo_id: str = Field(..., example="omanyasa/bantu-lang-id-model")
    model_path: str = Field(..., example="./models/my_model")

class LangIdRequest(BaseModel):
    text: str = Field(..., example="Ndiri kudzidza chiShona.")

class PublisherResponse(BaseModel):
    message: str
    url: str

class LangIdResponse(BaseModel):
    language: str
    confidence: float
    text: str

# --- Dependencies ---

def get_hf_token():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise HTTPException(status_code=500, detail="HF_TOKEN environment variable not set.")
    return hf_token

# --- API Endpoints ---

@app.post("/identify/", response_model=LangIdResponse)
async def identify_language_endpoint(request: LangIdRequest):
    """
    Identifies the language of a given text.
    """
    result = identify_language(request.text)
    return result

@app.post("/publish/dataset/", response_model=PublisherResponse)
async def publish_dataset_endpoint(dataset: DatasetPublishRequest, hf_token: str = Depends(get_hf_token)):
    """
    Publishes a dataset to the Hugging Face Hub.
    """
    try:
        publish_dataset(
            hf_token=hf_token,
            repo_id=dataset.repo_id,
            dataset_files=dataset.dataset_files,
            readme_file=dataset.readme_file
        )
        return {
            "message": "Dataset successfully published!",
            "url": f"https://huggingface.co/datasets/{dataset.repo_id}"
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/publish/model/", response_model=PublisherResponse)
async def publish_model_endpoint(model: ModelPublishRequest, hf_token: str = Depends(get_hf_token)):
    """
    Publishes a model to the Hugging Face Hub.
    """
    try:
        publish_model(
            hf_token=hf_token,
            repo_id=model.repo_id,
            model_path=model.model_path
        )
        return {
            "message": "Model successfully published!",
            "url": f"https://huggingface.co/{model.repo_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Language Services API. Go to /docs for API documentation."}

