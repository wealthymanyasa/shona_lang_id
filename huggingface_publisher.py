# huggingface_publisher.py (compatible with huggingface_hub 1.1.5)
import os
import shutil
from huggingface_hub import login, HfApi

def publish_dataset(hf_token, repo_id, dataset_files, readme_file="README.md", local_dir="hf_dataset_upload"):
    # 1️⃣ Login
    login(token=hf_token)
    print("Logged in to Hugging Face Hub.")

    # 2️⃣ Prepare local folder
    os.makedirs(local_dir, exist_ok=True)

    # Copy dataset files
    for file_path in dataset_files:
        if os.path.isfile(file_path):
            shutil.copy(file_path, local_dir)
            print(f"Copied {file_path} to {local_dir}")
        else:
            print(f"WARNING: File not found: {file_path}")

    # Copy README
    if os.path.isfile(readme_file):
        shutil.copy(readme_file, local_dir)
        print(f"Copied {readme_file} to {local_dir}")
    else:
        print(f"WARNING: README file not found: {readme_file}")

    # 3️⃣ Create repo if it doesn't exist
    api = HfApi()
    api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)
    print(f"Dataset repo {repo_id} ready.")

    # 4️⃣ Upload files individually (better for large files)
    for filename in os.listdir(local_dir):
        file_path = os.path.join(local_dir, filename)
        print(f"Uploading {filename}...")
        api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=filename,
            repo_id=repo_id,
            repo_type="dataset",
            token=hf_token
        )
        print(f"Uploaded {filename} ✅")

    print(f"Dataset successfully pushed: https://huggingface.co/datasets/{repo_id}")


if __name__ == "__main__":
    # Get token from environment variable for security
    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        raise ValueError("Please set HF_TOKEN environment variable with your Hugging Face token")
    
    REPO_ID = "omanyasa/bantu-lang-id"
    FILES = [
        "data/shona_en_lang_train.txt",
        "data/shona_en_lang_valid.txt",
        "data/shona_en_lang_test.txt"
    ]
    README = "README.md"

    publish_dataset(HF_TOKEN, REPO_ID, FILES, readme_file=README)
