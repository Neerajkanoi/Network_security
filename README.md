# 🛡️ Network Security — Phishing Website Detection
 
An end-to-end **MLOps pipeline** that detects phishing websites from URL/website-based features. The project covers the full lifecycle of a machine learning system — data ingestion, validation, transformation, model training and experiment tracking, a REST API for training/inference, containerization, and CI/CD deployment to AWS.
 
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248.svg)](https://www.mongodb.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED.svg)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Deployment-FF9900.svg)](https://aws.amazon.com/)
 
---
 
## 📋 Table of Contents
 
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pipeline Stages](#-pipeline-stages)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Future Improvements](#-future-improvements)
---
 
## 🔍 Overview
 
Phishing websites are one of the most common attack vectors for credential theft and fraud. This project trains a **binary classification model** on a set of extracted website/URL features (e.g. use of an IP address instead of a domain, URL length, presence of `@` symbols, SSL certificate status, domain age, redirects, iframe usage, etc.) to predict whether a given site is **phishing** or **legitimate**.
 
Rather than a one-off notebook, the project is structured as a **production-style ML system**:
 
- Raw data lives in **MongoDB**, not a static file.
- A modular **training pipeline** (ingestion → validation → transformation → model training) produces a versioned, reproducible model.
- Every experiment is logged to **MLflow** (hosted via DagsHub) for comparison and auditability.
- A **FastAPI** service exposes the pipeline for on-demand retraining and batch inference.
- The whole app is **containerized** and deployed via **GitHub Actions CI/CD** to AWS.
---
 
## 🏗️ Architecture
 
```
Local CSV (Network_data/phisingData.csv)
        │
        │  push_data.py
        ▼
   MongoDB Atlas  ───────────────────────────────►  Single source of truth for raw data
        │
        │  main.py → TrainingPipeline
        ▼
 ┌────────────────────────────────────────────────────────────┐
 │ 1. Data Ingestion      → pull from MongoDB, train/test split │
 │ 2. Data Validation     → schema checks + data drift report   │
 │ 3. Data Transformation → imputation, preprocessing pipeline  │
 │ 4. Model Trainer       → train & compare models, log to      │
 │                          MLflow/DagsHub, export best model   │
 └────────────────────────────────────────────────────────────┘
        │
        ▼
 final_model/  (preprocessor.pkl + model.pkl)
        │
        ▼
     app.py (FastAPI)
   ┌───────────────┬──────────────────┐
   │   GET /train   │   POST /predict   │
   │  re-runs the    │   scores an       │
   │  full pipeline   │   uploaded CSV     │
   └───────────────┴──────────────────┘
        │
        ▼
 Docker → GitHub Actions CI/CD → AWS (ECR + EC2)
```
 
---
 
## 🧰 Tech Stack
 
| Category | Technology |
|---|---|
| Language | Python 3.10 |
| Data Storage | MongoDB (Atlas) |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn |
| Experiment Tracking | MLflow + DagsHub |
| Object Serialization | dill |
| Configuration | PyYAML (`data_schema/schema.yaml`) |
| API Framework | FastAPI + Uvicorn |
| Templating | Jinja2 |
| Secrets Management | python-dotenv |
| Packaging | setuptools (`setup.py`) |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Cloud / Deployment | AWS (ECR, EC2, AWS CLI) |
 
---
 
## 📁 Project Structure
 
```
Network_security/
├── networksecurity/            # Core installable Python package
│   ├── components/              # Pipeline stage logic (ingestion, validation, transformation, trainer)
│   ├── entity/                  # Config & artifact dataclasses (typed contracts between stages)
│   ├── pipeline/                 # Pipeline orchestration
│   ├── exception/                 # Custom exception handling
│   ├── logging/                    # Centralized logging setup
│   ├── utils/                       # Shared utilities (save/load objects, YAML readers, model estimator)
│   └── constant/                     # Central constants (paths, DB/collection names, column names)
├── data_schema/                       # schema.yaml — expected columns & dtypes
├── Network_data/                        # Raw source dataset (phisingData.csv)
├── Artifacts/                             # Timestamped outputs from each pipeline run
├── final_model/                            # Production-ready model + preprocessor
├── logs/                                    # Runtime log files
├── .github/workflows/                        # CI/CD pipeline definitions
├── app.py                                     # FastAPI application (train & predict endpoints)
├── main.py                                     # CLI entry point to run the full training pipeline
├── push_data.py                                 # Utility script to load CSV data into MongoDB
├── setup.py                                      # Package configuration
├── requirements.txt                               # Project dependencies
├── Dockerfile                                      # Container build definition
└── test_db.py                                       # MongoDB connection sanity check
```
 
---
 
## ⚙️ Pipeline Stages
 
1. **Data Ingestion** — Connects to MongoDB, reads the raw collection into a DataFrame, exports it to a feature store, and splits it into train/test sets.
2. **Data Validation** — Validates the train/test data against `schema.yaml` (column count, names, dtypes) and generates a data drift report between the two sets.
3. **Data Transformation** — Applies preprocessing (imputation of missing values, feature preparation) and serializes the fitted preprocessing pipeline.
4. **Model Trainer** — Trains and compares multiple classification models, selects the best performer, logs parameters/metrics/artifacts to MLflow (via DagsHub), and exports the final model and preprocessor to `final_model/`.
Each stage consumes the previous stage's **artifact** and produces its own — a clean, testable, and reproducible pipeline design.
 
---
 
## 🚀 Getting Started
 
### Prerequisites
 
- Python 3.10+
- A MongoDB Atlas cluster (or local MongoDB instance)
- (Optional) A DagsHub account for MLflow tracking
### Installation
 
```bash
# Clone the repository
git clone https://github.com/Neerajkanoi/Network_security.git
cd Network_security
 
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
 
# Install dependencies
pip install -r requirements.txt
```
 
### Environment Variables
 
Create a `.env` file in the project root:
 
```env
MONGO_DB_URL=<your-mongodb-connection-string>
MONGODB_URL_KEY=<your-mongodb-connection-string>
```
 
### Load Data into MongoDB
 
```bash
python push_data.py
```
 
### Run the Training Pipeline
 
```bash
python main.py
```
 
---
 
## 🖥️ Usage
 
### Run the API locally
 
```bash
python app.py
```
 
The API will be available at `http://localhost:8000`. Visiting the root URL redirects to the interactive Swagger docs at `http://localhost:8000/docs`.
 
---
 
## 📡 API Reference
 
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to interactive API docs (`/docs`) |
| `GET` | `/train` | Triggers a full run of the training pipeline |
| `POST` | `/predict` | Accepts a CSV file upload and returns predictions as an HTML table |
 
**Example — predict via cURL:**
 
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: text/html" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_data.csv"
```
 
---
 
## ☁️ Deployment
 
The project is containerized with Docker and deployed via a GitHub Actions CI/CD pipeline:
 
1. **Build** — Docker image is built from the `Dockerfile` (`python:3.10-slim-bookworm` base).
2. **Push** — Image is pushed to **AWS ECR** (Elastic Container Registry).
3. **Deploy** — A self-hosted GitHub Actions runner on an **AWS EC2** instance pulls the new image and restarts the container.
```bash
# Build the image locally
docker build -t network-security-app .
 
# Run the container
docker run -p 8000:8000 --env-file .env network-security-app
```
 
Secrets such as `MONGO_DB_URL` and AWS credentials are managed via **GitHub Secrets** and never committed to source control.
 
---
 
## 🔮 Future Improvements
 
- [ ] Add authentication to the `/train` endpoint
- [ ] Load the model into memory once at startup rather than per-request
- [ ] Add automated unit tests for each pipeline component
- [ ] Validate `/predict` input against the schema before inference
- [ ] Introduce an MLflow Model Registry for versioning and rollback
- [ ] Add monitoring for prediction drift in production
- [ ] Return predictions as JSON in addition to HTML
---
 
## 📄 License
 
This project currently has no license specified. Consider adding one (e.g., MIT) if you intend for others to use or contribute to it.
 
---
 
## 🙋 Author
 
**Neeraj Kanoi** — [GitHub](https://github.com/Neerajkanoi)
 
