# AI Catalog Assistant

An AI catalog assistant with a React frontend and a FastAPI backend. The app includes live product suggestions, CSV catalog upload and question answering, product administration, and browser-based voice input and speech output.

## Project contents

- `main.py`, `rag.py`, and `llm.py`: FastAPI API, CSV search, and local language model.
- `frontend/`: React user interface.
- `trained_assistant/`: model configuration, tokenizer, and trained model weights.
- `products.json` and `general_qa_100000_multi_domain.json`: product data and training dataset.
- `uploaded_catalogs/`: bundled example catalog CSVs for testing catalog questions.
- `train.py`: model training script.

The trained model weights are stored with Git LFS because the model file exceeds GitHub's regular file size limit. Install Git LFS before cloning this repository. If GitHub reports that the account's LFS storage or bandwidth quota has been reached, the model will need to be hosted separately.

## Requirements

- Python 3.11 or later.
- Node.js and npm.
- Git and Git LFS.
- A microphone and internet access for the optional voice-input feature.

## Run the backend

From the project root, create and activate a Python virtual environment, then install the dependencies:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Its interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Run the frontend

In a second terminal, install the frontend dependencies and start the React app:

```powershell
cd frontend
npm ci
npm start
```

The frontend runs at `http://localhost:3000` and connects to the backend at `http://127.0.0.1:8000`.

## Train the model

`train.py` uses the included JSON dataset and saves training output under `trained_assistant/`. The training script currently requires a CUDA-enabled GPU. Install the appropriate PyTorch build for your CUDA setup before training.

## Local data and secrets

The bundled example catalog CSVs are included; additional uploaded catalog files and generated audio are kept locally and excluded from Git. Add local credentials to an `.env` file if needed; `.env` files are ignored. Never commit API keys, passwords, access tokens, or private catalog data.
