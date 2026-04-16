<h3 align="center">ChurnLabs : Customer Churn Prediction</h3>

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live-Demo-00C7B7?style=flat&logo=netlify&logoColor=white)](https://churnlabs.netlify.app)
[![API Docs](https://img.shields.io/badge/API-Docs-009688?style=flat&logo=fastapi&logoColor=white)](https://churnlabs.onrender.com/docs)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-Image-2496ED?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/r/themrityunjaypathak)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![uv](https://img.shields.io/badge/uv-Astral-D7FF64?style=flat)](https://docs.astral.sh/uv/)
[![React](https://img.shields.io/badge/React-333A45?style=flat&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)](https://git-scm.com/)

</div>

<a href="https://churnlabs.netlify.app"><img title="ChurnLabs" src="https://github.com/user-attachments/assets/88d4eeb6-3367-4e87-8932-a6a3624225d2"></a>

## Table of Contents
- [Problem Statement](#problem-statement)
- [Quick Start](#quick-start)
- [Workflow](#workflow)
- [Impact](#impact)
- [Setup](#setup)
- [Config-Driven Design](#config-driven-design)
- [Dependency Management](#dependency-management)
- [Makefile](#makefile)
- [Experiment Tracking](#experiment-tracking)
- [Model Training & Evaluation](#model-training--evaluation)
- [Folder Structure](#folder-structure)
- [License](#license)

<hr>

## Problem Statement
- Many companies struggle to accurately identify customers who are likely to discontinue their services.
- Missed churn signals lead to customer attrition, directly impacting revenue and long-term business growth.
- This project aims to identify high-risk customers early, enabling businesses to take proactive retention measures.

<hr>

## Quick Start
- Run the entire project locally with a few simple commands :
```bash
git clone https://github.com/themrityunjaypathak/ChurnLabs.git
cd ChurnLabs

make install-dev     # Install dependencies and setup virtual environment

make ingest          # Fetch data from PostgreSQL (or skip if using local dataset)
make preprocess      # Clean and transform the data
make train           # Train the model

make api-dev         # Start FastAPI backend
make frontend-dev    # Start React frontend
```
- Once the services are running, open the following URLs :

**React Frontend**
```
http://localhost:5173
```
**FastAPI Backend**
```
http://localhost:8000
```

> [!NOTE]
> Ensure that the PostgreSQL database is running and correctly configured before running ingestion.

> [!IMPORTANT]
> The default pipeline expects data to be ingested from a configured PostgreSQL database.
>
> If you don't have a PostgreSQL database configured, you can use a local dataset instead :
>
> - Download the dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
>
> - Place the dataset at : `data/raw/customer-churn-raw.csv`
>
> - Ensure the filename matches exactly as : `customer-churn-raw.csv`
> 
> Then run the preprocessing pipeline :
>
> ```bash
> make preprocess
> ```
>
> This will use the local dataset instead of the PostgreSQL database and proceed with preprocessing.

> [!TIP]
> You can also start the entire application using Docker :
>
> ```bash
> make compose-up-build
> ```
>
> Once the services are running, open the following URLs :
>
> - React Frontend : `http://localhost:3000`
> 
> - FastAPI Backend : `http://localhost:8000`

<hr>

## Workflow

<img title="Workflow Diagram" src="https://github.com/user-attachments/assets/080a25b1-2929-409b-bdba-15302b03c4b7">

<hr>

## Impact
- Achieved ~90% recall for churn, improving early identification of high-risk customers and reducing missed churn.
- Optimized decision threshold to prioritize recall, aligning model performance with retention-focused objectives.
- Enables targeted retention by identifying customers most likely to churn, improving retention effectiveness.
- Deployed a real-time churn prediction system, enabling immediate churn risk assessment during decision making.

<hr>

## Setup

### 1. Clone the Repository
- First, you need to clone the project from GitHub to your local system.
```bash
git clone https://github.com/themrityunjaypathak/ChurnLabs.git
```

<hr>

### 2. Install Dependencies
- This project uses `uv` for dependency management.
- `uv` is a modern Python package manager that is significantly faster than `pip`.
- Install `uv` if not already installed :
```bash
pip install uv
```
- Then install all project dependencies :
```bash
make install-dev
```

### What happens during this process?
- Create an isolated virtual environment (`.venv`).
- Install all project dependencies (including development tools).
- Sync package versions with `pyproject.toml` and `uv.lock`.
- Ensure a fully reproducible and consistent environment.

<hr>

### 3. Run Data Ingestion
- This step extracts raw customer data from the PostgreSQL database,
- And stores it locally for further processing.
- Run the ingestion pipeline :
```bash
make ingest
```

### What happens during ingestion?
- Connects to a PostgreSQL database using credentials stored in `.env`.
- Fetches customer churn data required for model training and evaluation.
- Stores raw dataset locally at `data/raw/customer-churn-raw.csv`.

> [!NOTE]
> Ensure that the PostgreSQL database is running and correctly configured before running ingestion.

> [!IMPORTANT]
> The ingestion step requires access to a PostgreSQL database.
>
> If you do not have access to the original database, you have two options :
>
> 1. Use your own PostgreSQL database
>    - Upload the [dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) to your database.
>    - Configure credentials in the `.env` file.
>    - Run `make ingest` to ingest the data locally.
>
> 2. Skip ingestion and use dataset directly
>    - Download the [dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) from Kaggle.
>    - Place it inside `data/raw/` as `customer-churn-raw.csv`.
>    - Skip ingestion and continue with preprocessing and training.
>
> This ensures the project remains fully reproducible even without database access.

<hr>

### 4. Run Data Preprocessing
- This step transforms the raw dataset into a structured format suitable for model training.
- Run the preprocessing pipeline :
```bash
make preprocess
```

### What happens during preprocessing?
1. Load Raw Dataset
```
data/raw/customer-churn-raw.csv
```
2. Validate Schema
- Checks :
    - Feature Consistency
    - Missing Values
    - Data Types
    - Categorical Levels
3. Clean the Dataset
- Typical cleaning steps include :
    - Removing Invalid Records
    - Encoding Categorical Features
    - Trimming Whitespace
    - Type Conversions
4. Export Processed Dataset
- The processed dataset is saved to :
```
data/processed/customer-churn-processed.parquet
```

<hr>

### 5. Run Model Training
- This step trains and evaluates the churn prediction model, generating artifacts for inference and deployment.
- Run the training pipeline :
```bash
make train
```

### What happens during training?
1. Load Processed Dataset
```
data/processed/customer-churn-processed.parquet
```
2. Split data into training and testing sets.
3. Build a Scikit-learn Pipeline that combines :
    - Preprocessing
    - Feature Engineering
    - Model Training and Evaluation
4. Run cross-validation to evaluate model performance.
5. Apply decision threshold tuning to optimize recall.
6. Save the trained model and evaluation metrics as artifacts.

### Generated Artifacts
- After training, the following files are created :
```
artifacts/models/pipe.joblib
artifacts/metrics/metrics.json
```
**`pipe.joblib`**
- Serialized Scikit-learn Pipeline
- Used by the `/predict` endpoint for inference

**`metrics.json`**
- Training Metadata that contains :
    - Evaluation Metrics
    - Decision Threshold
    - Model Version
    - Training Timestamp
- Used by the `/info` endpoint for providing training metadata

### Upload Artifacts to Hugging Face
- After generating artifacts locally, the training pipeline uploads them to Hugging Face.
- This enables centralized storage and access in deployment environments.

### Artifacts Loading Strategy
The system follows a local-first loading strategy with remote fallback :
- Check for the local artifacts :
```
artifacts/models/
artifacts/metrics/
```
- If present ➜ load from local storage.
- If not present ➜ fetch from Hugging Face.

### Why this design?
- Enables seamless development using local artifacts.
- Avoids committing large binary files to the repository.
- Ensures production systems can operate without local dependencies.
- Provides a robust fallback mechanism for reliable model loading.

<hr>

### 6. MLflow Experiment Tracking
- The project uses MLflow to track machine learning experiments.
- MLflow allows you to log :
    - Model Parameters
    - Evaluation Metrics
    - Experiment Artifacts
- Start the MLflow backend server :
```bash
make mlflow-ui
```
- Once the MLflow server starts, open the MLflow dashboard at :
```
http://localhost:5000
```
- Inside the dashboard you can :
    - Compare Multiple Experiment Runs
    - Visualize Evaluation Metrics
    - Inspect Experiment Artifacts

<img title="MLflow Dashboard" src="https://github.com/user-attachments/assets/35a086b4-f3af-48fe-9a79-c85eda64ce5f">

<hr>

### 7. Start the FastAPI Backend
- The FastAPI server loads the trained model and expose endpoints for inference and system health.
- Run the FastAPI backend server :
```bash
make api-dev
```
- Once the server starts, open the FastAPI documentation at :
```
http://localhost:8000/docs
```
- This interactive Swagger UI allows you to test endpoints directly.

> [!IMPORTANT]
> The FastAPI server exposes the following endpoints :
>
> **1. Root Endpoint (`/`)**
> 
> - Returns a simple response confirming that the API is running.
>
> **2. Health Check Endpoint (`/health`)**
> 
> - Verifies that the API service is active and the model is successfully loaded.
>
> **3. Model Metadata Endpoint (`/info`)**
> 
> - Returns information about the trained model, like model version, training timestamp, and other metadata.
>
> **4. Churn Prediction Endpoint (`/predict`)**
> 
> - Accepts customer data as input and returns the churn probability, predicted class, and the decision threshold.

> [!TIP]
> When deploying the backend on Render, make sure to configure the secrets in the Render dashboard.
>
> Navigate to : **Render Dashboard → Your Service → Environment → Environment Variables**
>
> Add the following environment variables :
>
> ```
> ENV=your_env_name
> PORT=your_api_port
> ALLOWED_ORIGINS=your_allowed_origins
> ```
>
> `ALLOWED_ORIGINS` is used to configure CORS so that the deployed React frontend can communicate with the API.

> [!NOTE]
>
> The API for this project is deployed on the free tier of Render.
>
> Services on the free tier automatically go to sleep after periods of inactivity.
>
> If the API is asleep, open the API URL once to wake the server.
>
> After the service starts, you can navigate to the website and generate predictions normally.

Access the live API documentation [here](https://churnlabs.onrender.com/docs) or Click on the Image below.

<a href="https://churnlabs.onrender.com/docs"><img title="Swagger UI" src="https://github.com/user-attachments/assets/0ce583ab-55a3-421d-9504-43e3bd15831f"></a>

<hr>

### 8. Start the React Frontend
- The frontend provides an interactive UI for generating real-time churn predictions.
```bash
make frontend-dev
```
- This command installs the Node dependencies and starts the React development server at :
```
http://localhost:5173
```
- The frontend communicates with the FastAPI backend to send requests and display predictions.

> [!TIP]
> The project includes a `netlify.toml` file for seamless frontend deployment on Netlify.
>
> ```toml
> [build]
>   base = "frontend"
>   command = "npm run build"
>   publish = "dist"
> ```
>
> This configuration tells Netlify to :
>
> - Build the application inside the `frontend` directory.
> - Execute the `npm run build` command.
> - Deploy the output from the `dist` folder.
>
> Learn more about Netlify Configuration [here](https://docs.netlify.com/configure-builds/file-based-configuration/).

> [!NOTE]
> When deploying the frontend on Netlify, make sure to configure the secrets in the Netlify dashboard.
>
> Navigate to : **Netlify Dashboard → Site Settings → Environment Variables**
>
> ```bash
> VITE_API_URL=your_base_api_url
> ```
>
> This variable defines the base API url that the React frontend will use for generating predictions.
>
> Without this variable, the frontend will still attempt to connect to the local API (`localhost:8000`).

Access the live application [here](https://churnlabs.netlify.app) or Click on the Image below.

<a href="https://churnlabs.netlify.app"><img title="React Frontend" src="https://github.com/user-attachments/assets/f5760807-0c32-4d2f-bcf8-e94423ec3e80"></a>

<hr>

### 9. Start Entire Application with Docker
- Instead of running services manually, you can start the entire application using Docker.
```bash
make compose-up-build
```
- Docker compose will build and start all required services for the application using `docker-compose.yaml`.

### React Frontend
```
http://localhost:3000
```
### FastAPI Backend
```
http://localhost:8000
```

<img title="Docker Compose" src="https://github.com/user-attachments/assets/068c312b-a626-479c-9c87-f2776fc64e5e">

<hr>

### 10. Push Entire Application to Docker Hub
- This step builds and pushes both the backend and frontend images to Docker Hub using `docker-compose.yaml`.
- Ensure Docker is installed and running.
- Make sure you are logged in to Docker Hub using :
```bash
make docker-login
```

### Build Docker Images
- Build both backend and frontend images as defined in `docker-compose.yaml` :
```bash
make compose-build
```

### Push Docker Images
- Push both images to Docker Hub :
```bash
make compose-push
```

### What happens during this process?
- Builds the backend image using `api/Dockerfile`
- Builds the frontend image using `frontend/Dockerfile`
- Tags images using the names defined in `docker-compose.yaml` :
```
themrityunjaypathak/churnlabs-api:v1
themrityunjaypathak/churnlabs-frontend:v1
```
- Pushes both images to your Docker Hub repositories.

> [!NOTE]
>
> Ensure that the `image:` field is correctly defined for each service in `docker-compose.yaml`.
> 
> Without it, Docker Compose will not be able to push images to Docker Hub.

> [!TIP]
> You can verify the pushed images on Docker Hub.
> 
> View the Backend Docker Image [here](https://hub.docker.com/r/themrityunjaypathak/churnlabs-api) or Click on the Image below.
>
> <a href="https://hub.docker.com/r/themrityunjaypathak/churnlabs-api"><img title="Backend Docker Image" src="https://github.com/user-attachments/assets/cbb1c20d-4eba-4b73-89fb-4f52ae951d41"></a>
>
> View the Frontend Docker Image [here](https://hub.docker.com/r/themrityunjaypathak/churnlabs-frontend) or Click on the Image below.
>
> <a href="https://hub.docker.com/r/themrityunjaypathak/churnlabs-frontend"><img title="Frontend Docker Image" src="https://github.com/user-attachments/assets/adb254b5-b357-4977-b0cf-0d5fa6e7eb42"></a>

<hr>

### 11. Stop the Application
- This step stops and removes all running containers.
```bash
make compose-down
```
- It frees up system resources and shuts down the application services.

<hr>

## Config-Driven Design
- This project adopts a config-driven approach to manage data, model, training and artifacts.
- Instead of hardcoding values inside the codebase, these settings are stored in YAML configuration files.
- These files are loaded during preprocessing, training, inference and artifacts logging.
```
config/
├── data-config.yaml
├── model-config.yaml
├── training-config.yaml
├── huggingface-config.yaml
└── artifacts-config.yaml
```

<img title="Config Files" src="https://github.com/user-attachments/assets/f7b07aca-ac4d-4f22-b7aa-a822d8f674e3">

### Why this is useful?

### 1. Cleaner Code
- Configuration values are separated from pipeline logic.
- Instead of writing :
```python
test_size = 0.2
random_state = 42
threshold = 0.42
```
- The values are stored in a configuration file.
```yaml
training:
  test_size: 0.2
  random_state: 42

threshold:
  value: 0.42
```
- The code simply loads them.
```python
config = get_training_config()
random_state = config["training"]["random_state"]
```

### 2. Easier Experimentation
- You can modify parameters without changing the code.
```yaml
threshold:
  value: 0.32
```
- Changing this value updates the model behavior without touching the training pipeline.

### 3. Better Reproducibility
- All settings are stored in configuration files, making it easier to reproduce experiments consistently.

### 4. Scalable Project Structure
- As the project grows, new models or parameters can be added easily.
- Simply extend the configuration files without modifying the core codebase.

<hr>

## Dependency Management
- This project uses `uv` for dependency management instead of traditional tools like `pip`.
- `uv` is a modern package manager designed for speed, reproducibility, and simplicity.
- It simplifies the Python workflow by combining :
	- Dependency Management
	- Virtual Environment Handling
	- Package Installation
	- Command Execution
- into a single tool.

<img title="uv by Astral" src="https://github.com/user-attachments/assets/0f061d2f-78d2-4bcc-9a48-70cf5700fc68">

### Why use `uv` over `pip`?

### 1. Faster Dependency Installation
- `uv` is significantly faster than `pip` due to its optimized resolver and parallel installation.
- This reduces setup time, especially for large projects with many dependencies.
```bash
uv sync
```

### 2. Reproducible Environments
- Dependencies are locked in the `uv.lock` file.
- Ensures the same versions are installed across different systems.
```bash
uv lock
uv sync
```
> [!NOTE]
> This guarantees consistent behavior across development, testing, and deployment environments.

### 3. Automatic Virtual Environment Management
- `uv` automatically creates and manages a virtual environment.
- No need to manually run `python -m venv .venv`.
```bash
uv sync
```
> [!TIP]
> By default, the virtual environment is created inside the `.venv` directory.

<hr>

## Makefile
- A Makefile is a configuration file used by the `Make` build automation tool.
- It defines reusable commands called targets.
- Each target represents a specific task, such as :
    - Installing Dependencies
    - Running Training Pipeline
    - Starting FastAPI Backend Server
    - Launching MLflow Dashboard
- Instead of manually running multiple commands, `Make` executes them automatically.

### Why use a Makefile?
- Using a Makefile improves the development workflow by simplifying command execution.
- Instead of running long commands like :
```python
uv run python scripts/run_training.py
```
- You can simply run :
```bash
make train
```

### Using the Makefile
- You can view all available `Make` commands by running :
```bash
make help
```
- This will display all supported tasks defined in the Makefile.

### Setup `Make` for Windows
- Windows does not include the `Make` utility by default.
- The easiest and most reliable way to use `Make` is through WSL.

<details>
<summary>Click Here for More Details</summary>

### Step 1 : Open PowerShell as Administrator
- Open the Start Menu
- Search for PowerShell
- Run it as Administrator

### Step 2 : Install WSL
- Run the following command :
```bash
wsl --install
```
- This command will :
    - Enable WSL on Windows
    - Install the Linux Kernel
    - Install Ubuntu as the default Linux Distribution
- After installation finishes, you may be prompted to restart your computer.

### Step 3 : Launch Ubuntu
- After restarting :
    - Open the Start Menu
    - Search for Ubuntu
    - Launch the App
- The first launch may take a few minutes.
- When Ubuntu runs for the first time, it will ask you to create a Linux user :
```bash
Enter new UNIX username: your_username
New password: your_password
```
- This sets up your Linux environment inside Windows.

### Step 4 : Update Ubuntu Packages
- Before installing any software, update the package manager.
```bash
sudo apt update
```
- Then upgrade installed packages :
```bash
sudo apt upgrade -y
```
- This ensures your Linux environment is up to date.

### Step 5 : Install Make
- Now install the GNU `Make` build tool.
```bash
sudo apt install build-essential -y
```
- `Make` will now be available in your WSL environment.

### Step 6 : Verify Make Installation
- Check that `Make` was installed correctly :
```bash
make --version
```
- You should see output similar to :
```bash
GNU Make 4.x
Built for x86_64-pc-linux-gnu
```
- This confirms that `Make` is installed successfully.
- Remember `Make` is available only inside the WSL terminal, not in Windows Command Prompt or PowerShell.

</details>

### Setup WSL in VS Code

<details>
<summary>Click Here for More Details</summary>

### Step 1 : Install WSL Extension
- Open VS Code
- Go to Extensions (Ctrl + Shift + X)
- Search for : `WSL by Microsoft`
- Click Install

### Step 2 : Restart VS Code
- After installing the extension :
	- Close VS Code
 	- Reopen it

### Step 3 : Check Terminal Profiles
- Open terminal : `Ctrl + ~`
- Click the dropdown (next to +)
- You should now see something like :
```
Ubuntu (WSL)
```

</details>

<hr>

## Experiment Tracking
- This project uses MLflow to track machine learning experiments, compare models, and log artifacts.
- MLflow helps maintain reproducibility and transparency by tracking model parameters, evaluation metrics, etc.
- Instead of manually tracking result in notebooks,
- MLflow provides a centralized dashboard to analyze and compare model performance.

### Start the MLflow Dashboard
- To start the MLflow dashboard locally, run the following command from the project root directory :
```bash
make mlflow-ui
```
- This command starts the MLflow tracking server using the local experiment database (`mlflow.db`).
- Once the server starts successfully, open the MLflow dashboard in your browser at :
```bash
http://localhost:5000
```
- The MLflow dashboard allows you to explore experiment runs and compare model results.

<img title="MLflow UI" src="https://github.com/user-attachments/assets/30a4f665-84b6-45bb-8b50-db89c96ee5b2">

### Types of Experiments Performed
- During model development, two types of experiments were performed and tracked using MLflow.

### 1. Model Comparison
- MLflow makes it easy to compare multiple models trained during experimentation.
- For this project, several classification models were evaluated, including :
    - Logistic Regression
    - K-Nearest Neighbors
    - Support Vector Classifier
    - Decision Tree
    - Random Forest
    - Gradient Boosting
- The dashboard allows sorting models by evaluation metrics such as :
    - Accuracy
    - Precision
    - Recall
    - ROC-AUC
    - PR-AUC
- This helps identify the best-performing model based on business requirements.

<img title="Model Comparison" src="https://github.com/user-attachments/assets/0a30ad8b-458a-41c3-bfc4-b766d7e2bf52">

### 2. Threshold Optimization
- After selecting the best-performing model, another experiment is conducted to optimize the decision threshold.
- Instead of using the default classification threshold of 0.5,
- Multiple thresholds were evaluated to improve the model's ability to detect churn.
- These experiments focused on :
    - Analyzing recall across different thresholds.
    - Selecting a threshold that meets business requirements.
    - Balancing precision-recall trade-offs.
- Optimal threshold selection allowed the model to achieve 90% recall for the churn class.

<img title="Threshold Optimization" src="https://github.com/user-attachments/assets/6753c497-6e2b-4b90-bcc3-5a1be9fdc453">

### Logged Artifacts
- MLflow also stores experiment artifacts generated during training.
- Some of the artifacts logged in this project include confusion matrix & classification reports.
- These artifacts help analyze model behavior and support model selection.

> [!IMPORTANT]
> You can also reset MLflow experiments and remove stored runs for newer ones.
>
> To reset MLflow experiments, run this command from the project root directory :
> 
> ```bash
> make mlflow-clean
> ```
>
> Resetting MLflow means permanently deleting all experiments, runs, metrics, and artifacts stored locally.

<hr>

## Model Training & Evaluation

### 1. Load the Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Importing load_processed_data function from loaders module
from churnlabs.data.loaders import load_processed_data
df = load_processed_data()
df.head()
```
</details>

<hr>

### 2. Split the Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Splitting Data into Training and Testing Set
from churnlabs.features.split import split_data
X_train, X_test, y_train, y_test = split_data(df)
```
</details>

<hr>

### 3. Encode Target Variable

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Encoding Target Variable (Yes/No -> 1/0)
from churnlabs.models.encoder import target_encoder
y_train, y_test = target_encoder(y_train, y_test)
```
</details>

<hr>

### 4. Build Preprocessing Pipeline

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Transformation for Categorical Columns
cat_cols = X_train.select_dtypes(include='category').columns

cat_trf = Pipeline(steps=[
    ('ohe', OneHotEncoder(sparse_output=False, drop='first'))
])
```
```python
# Transformation for Numerical Columns
num_cols = [col for col in X_train.select_dtypes(include='number').columns if col != 'seniorcitizen']

num_trf = Pipeline(steps=[
    ('scaler', StandardScaler())
])
```
```python
# Column Transformation
ctf = ColumnTransformer(transformers=[
    ('categorical', cat_trf, cat_cols),
    ('numerical', num_trf, num_cols)
], remainder='passthrough', n_jobs=-1)
```
```python
# Importing DummyClassifier Model
dummy = DummyClassifier(strategy='most_frequent', random_state=42)
```
```python
# Pipeline
pipe = Pipeline(steps=[
    ('preprocessor', ctf),
    ('model', dummy)
])
```
</details>

<hr>

### 5. Train Baseline Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Cross-Validation
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision',
    'recall': 'recall',
    'f1': 'f1',
    'roc_auc': 'roc_auc',
    'pr_auc': 'average_precision'
}

cv = cross_validate(estimator=pipe, X=X_train, y=y_train, cv=skf, scoring=scoring, n_jobs=-1)
```
```python
# Cross Validation Results
results = {metric.replace('test_', ''): [np.mean(scores), np.std(scores)] for metric, scores in cv.items() if metric.startswith('test')}
results_df = pd.DataFrame(results, index=['mean', 'std']).T
results_df
```

| | mean | std |
|:---:|:---:|:---:|
| accuracy | 0.7342 | 0.0 |
| precision	| 0.0000 | 0.0 |
| recall | 0.0000	| 0.0 |
| f1 | 0.0000 | 0.0 |
| roc_auc | 0.5000 | 0.0 |
| pr_auc | 0.2657	| 0.0 |

### What `DummyClassifier` helps us check?
- The `DummyClassifier` gives us a baseline to compare against real models.
- It predicts the majority class (`non-churn`) for every customer.
```
# Class Distribution
churn
No     0.7342
Yes    0.2657
```
```
# Classification Metrics
accuracy    0.73
precision   0.00
recall      0.00
f1          0.00
roc-auc     0.50
pr-auc      0.26
```
- Since the dataset contains approximately 73% non-churn customers, the model achieves 73% accuracy.
- However, it fails to identify any churners, resulting in `0` Precision, Recall, and F1 score.
- The ROC AUC of 0.5 confirms that the model has no predictive power and performs as a random guessing.
- The `DummyClassifier` makes exactly the same prediction in every fold.
- So every fold produces identical metrics, and that's why standard deviation is equal to 0.
- This confirms our pipeline and cross-validation setup behave as expected and no obvious leakage exists.
- Now any real model must surpass this benchmark to be considered a good performer.
```
# Real Model Expectations
Achieve PR AUC > 0.26
Achieve ROC AUC > 0.50
Achieve Precision > 0.00
Achieve Recall > 0.00
Achieve F1 Score > 0.00
```
- If a trained model cannot significantly outperform this baseline, it is not useful.
</details>

<hr>

### 6. Evaluate Multiple Models

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Multi-Model Dictionary 
models = {
    'dummy_classifier': DummyClassifier(strategy='most_frequent', random_state=42),
    'logistic_regression': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    'k_neighbors_classifier': KNeighborsClassifier(n_jobs=-1),
    'support_vector_classifier': SVC(class_weight='balanced', probability=True, random_state=42),
    'decision_tree_classifier': DecisionTreeClassifier(class_weight='balanced', random_state=42),
    'random_forest_classifier': RandomForestClassifier(class_weight='balanced', random_state=42, n_jobs=-1),
    'gradient_boosting_classifier': GradientBoostingClassifier(random_state=42)
}
```
```python
# Computing Average Metrics through Cross-Validation
results = {}

for name, model in models.items():
    
    pipe = Pipeline(steps=[
        ('preprocessor', ctf),
        ('model', model)
    ])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    cv_results = cross_validate(
        estimator=pipe,
        X=X_train,
        y=y_train,
        cv=skf,
        scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc', 'average_precision'],
        n_jobs=-1
    )

    model_results = {}
    for metric in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc', 'average_precision']:
        model_results[f"{metric}_mean"] = cv_results[f"test_{metric}"].mean()
        model_results[f"{metric}_std"] = cv_results[f"test_{metric}"].std()

    results[name] = model_results

results_df = pd.DataFrame(results).T
results_df
```
</details>

<hr>

### 7. Select `LogisticRegression` as Final Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Creating Logistic Regression Model Object
lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
```
```python
# Final Pipeline with Logistic Regression
pipe = Pipeline(steps=[
        ('preprocessor', ctf),
        ('model', lr)
    ])
```
```python
# Cross Val Predict
y_pred_cv = cross_val_predict(estimator=pipe, X=X_train, y=y_train, cv=skf, method='predict', n_jobs=-1)
```
```python
# Classification Report
print(classification_report(y_train, y_pred_cv, target_names=['No', 'Yes']))
```
```
              precision    recall  f1-score   support

          No       0.91      0.73      0.81      4130
         Yes       0.52      0.80      0.63      1495

    accuracy                           0.75      5625
   macro avg       0.72      0.77      0.72      5625
weighted avg       0.81      0.75      0.77      5625
```
```python
# Plotting Confusion Matrix
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
ConfusionMatrixDisplay.from_predictions(y_true=y_train, y_pred=y_pred_cv, display_labels=['No', 'Yes'], cmap='crest', ax=ax[0])
ConfusionMatrixDisplay.from_predictions(y_true=y_train, y_pred=y_pred_cv, display_labels=['No', 'Yes'], cmap='crest', normalize='all', ax=ax[1])
ax[0].set_title('Confusion Matrix (Counts)')
ax[1].set_title('Confusion Matrix (Normalized)')
ax[0].grid(visible=False)
ax[1].grid(visible=False)
plt.tight_layout()
plt.show()
```
<img title="Confusion Matrix Plot" src="https://github.com/user-attachments/assets/31c58541-5cc3-420e-883d-4796b7499c35">
</details>

<hr>

### 8. Feature Importance 

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Fitting Pipeline
pipe.fit(X_train, y_train)
```
```python
# Raw Column Names from ColumnTransformer (like 'numerical__totalcharges')
raw_features = pipe.named_steps['preprocessor'].get_feature_names_out()
```
```python
# Clean Column Names (splitting based on '__' and extracting 2nd element)
# ['numerical', 'totalcharges'] -> 'totalcharges'
features = [feature.split('__')[1] for feature in raw_features]
```
```python
# Coefficients from Logistic Regression
coefficients = pipe.named_steps['model'].coef_[0]
```
```python
# Feature Importance DataFrame
importance_df = pd.DataFrame({'feature': features, 'importance': coefficients}).sort_values(by='importance', ascending=False)
```
```python
# Feature Importance Plot
plt.figure(figsize=(12, 6))
colors = ['green' if val > 0 else 'red' for val in importance_df['importance']]
plt.barh(importance_df['feature'], importance_df['importance'], color=colors)
plt.xlabel('Impact on Log-Odds of Churn')
plt.title('Feature Importance Plot')
plt.axvline(0, linestyle='--')
plt.grid(axis='both', linestyle='--', alpha=1)
plt.tight_layout()
plt.show()
```
<img title="Feature Importance Plot" src="https://github.com/user-attachments/assets/fe447aab-ed24-4d03-9de2-4414e50bd441">
</details>

<hr>

### 9. Decision Threshold Optimization

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Cross Val Predict
y_proba_cv = cross_val_predict(estimator=pipe, X=X_train, y=y_train, cv=skf, method='predict_proba', n_jobs=-1)[:, 1]
```
```python
# Compute Precision-Recall Curve
precision, recall, thresholds = precision_recall_curve(y_train, y_proba_cv)
```
```python
# Align Threshold with Precision/Recall
pr_results = pd.DataFrame({
    "threshold": thresholds,
    "precision": precision[:-1],
    "recall": recall[:-1]
})
pr_results
```
```python
# Define a Recall Target (Business Decision)
recall_target = 0.90

# Evaluate Recall across Thresholds and Choose Best Threshold
valid = pr_results[pr_results["recall"] >= recall_target]

if not valid.empty:
    best_row = valid.loc[valid["precision"].idxmax()]
    best_threshold = best_row["threshold"]
else:
    best_threshold = 0.5

print(f"Best Threshold: {best_threshold:.4f}")
```
</details>

<hr>

### 10. Performance Evaluation using Tuned Threshold

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Cross Val Predict
y_proba_cv = cross_val_predict(estimator=pipe, X=X_train, y=y_train, cv=skf, method='predict_proba', n_jobs=-1)[:, 1]
```
```python
# Best Threshold
y_pred_best = (y_proba_cv >= best_threshold).astype(int)
```
```python
# Classification Report
print(classification_report(y_train, y_pred_best, target_names=['No', 'Yes']))
```
```
              precision    recall  f1-score   support

          No       0.94      0.61      0.74      4130
         Yes       0.45      0.90      0.60      1495

    accuracy                           0.69      5625
   macro avg       0.70      0.75      0.67      5625
weighted avg       0.81      0.69      0.70      5625
```
```python
# Plotting Confusion Matrix
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
ConfusionMatrixDisplay.from_predictions(y_train, y_pred_best, display_labels=['No', 'Yes'], cmap='crest', ax=ax[0])
ConfusionMatrixDisplay.from_predictions(y_train, y_pred_best, display_labels=['No', 'Yes'], cmap='crest', normalize='all', ax=ax[1])
ax[0].set_title('Confusion Matrix (Counts)')
ax[1].set_title('Confusion Matrix (Normalized)')
ax[0].grid(visible=False)
ax[1].grid(visible=False)
plt.tight_layout()
plt.show()
```
<img title="Confusion Matrix Plot" src="https://github.com/user-attachments/assets/75c9791d-a952-4d85-b443-497e89b82b4c">
</details>

<hr>

### 11. Final Evaluation on Test Set

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Fitting Pipeline on Full Training Data
pipe.fit(X_train, y_train)
```
```python
# Evaluate Final Model once on the Test Set
y_test_proba = pipe.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_proba >= best_threshold).astype(int)
```
```python
# Classification Report
print(classification_report(y_test, y_test_pred, target_names=['No', 'Yes']))
```
```
              precision    recall  f1-score   support

          No       0.93      0.59      0.72      1033
         Yes       0.44      0.89      0.59       374

    accuracy                           0.67      1407
   macro avg       0.69      0.74      0.65      1407
weighted avg       0.80      0.67      0.69      1407
```
```python
# Plotting Confusion Matrix
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred, display_labels=['No', 'Yes'], cmap='crest', ax=ax[0])
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred, display_labels=['No', 'Yes'], cmap='crest', normalize='all', ax=ax[1])
ax[0].set_title('Confusion Matrix (Counts)')
ax[1].set_title('Confusion Matrix (Normalized)')
ax[0].grid(visible=False)
ax[1].grid(visible=False)
plt.tight_layout()
plt.show()
```
<img title="Confusion Matrix Plot" src="https://github.com/user-attachments/assets/8dd991b1-8b00-4b42-bf79-1c6ad235f8a4">
</details>

<hr>

## Folder Structure

```
ChurnLabs/
│
├── api/                          # FastAPI backend for serving model predictions
│   ├── main.py                   # API endpoints (root, health, info, predict)
│   ├── schema.py                 # Pydantic schemas for request/response validation
│   ├── config.py                 # API configuration utilities
│   ├── utils.py                  # Helper functions used by the API
│   └── Dockerfile                # Dockerfile for the backend container
│
├── artifacts/                    # Saved model artifacts and evaluation metrics (ignored by Git)
│   ├── models/
│   │   └── pipe.joblib           # Trained ML pipeline used for prediction
│   │
│   └── metrics/
│       └── metrics.json          # Model evaluation metrics and metadata
│
├── config/                       # YAML configuration files
│   ├── artifacts-config.yaml     # Artifacts storage configuration
│   ├── data-config.yaml          # Data paths and database configuration
│   ├── huggingface-config.yaml   # Hugging Face model registry configuration
│   ├── model-config.yaml         # Model configuration and thresholds
│   └── training-config.yaml      # Training parameters and evaluation settings
│
├── data/                         # Project datasets (ignored by Git)
│   ├── raw/
│   │   └── customer-churn-raw.csv
│   │
│   └── processed/
│       └── customer-churn-processed.parquet
│
├── frontend/
│   ├── public/                   # Static assets used in the frontend
│   │   ├── favicon.svg
│   │   ├── hero-image.png
│   │   └── logo.png
│   │
│   ├── src/                      # React application source code
│   │   ├── App.tsx               # Main UI Component
│   │   ├── App.css               # Frontend styling
│   │   ├── main.tsx              # Application entry point
│   │   ├── index.css             # Global styling
│   │   │
│   │   └── assets/
│   │
│   ├── Dockerfile                # Dockerfile for the frontend container
│   ├── nginx.conf                # Nginx configuration for serving the frontend
│   ├── package.json              # Node.js dependencies
|   ├── package-lock.json         # Dependency lock file
│   ├── index.html                
│   ├── vite.config.ts            
│   ├── eslint.config.js          
│   ├── tsconfig.json             
│   ├── tsconfig.app.json         
│   ├── tsconfig.node.json        
│   ├── .env.example              # Example environment variables for frontend
│   ├── .gitignore                # Frontend-specific Git ignore rules
│   ├── .dockerignore             # Frontend Dockerignore rules
│   └── README.md                 
│
├── mlartifacts/                  # MLflow artifacts storage (ignored by Git)
│   └── ...                       # Auto-generated MLflow run directories
|
├── notebooks/                    # Jupyter notebooks for experimentation
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   └── 02_model.ipynb            # Model experimentation and MLflow tracking
│
├── scripts/                      # Executable python scripts
│   ├── run_ingestion.py          # Data ingestion pipeline
│   ├── run_preprocessing.py      # Data preprocessing pipeline
│   └── run_training.py           # Model training pipeline
│
├── src/
│   |
│   └── churnlabs/
│       │
│       ├── core/                 # Core utility module
|       |   ├── __init__.py
│       │   ├── config.py
│       │   ├── logger.py
│       │   └── settings.py
│       │
│       ├── data/                 # Data loading and preprocessing module
|       |   ├── __init__.py
│       │   ├── ingestion.py
│       │   ├── loaders.py
│       │   ├── preprocessor.py
│       │   └── export.py
│       │
│       ├── features/             # Feature engineering module
|       |   ├── __init__.py
│       │   └── split.py
│       │
│       ├── models/               # Model training and evaluation module
|       |   ├── __init__.py
│       |   ├── artifact.py
│       |   ├── builder.py
│       |   ├── encoder.py
│       |   ├── evaluation.py
│       |   ├── pipeline.py
│       |   ├── transformer.py
|       |   ├── loader.py
│       |   └── uploader.py
|       |
|       └── __init__.py
│
├── docker-compose.yaml           # Docker orchestration for backend and frontend
├── Makefile                      # Project commands (MLflow, FastAPI, React, Docker, etc.)
├── pyproject.toml                # Python project configuration
├── uv.lock                       # Dependency lock file
├── netlify.toml                  # Netlify deployment configuration
├── mlflow.db                     # MLflow experiment tracking database (ignored by Git)
│
├── .dockerignore                 # Backend Dockerignore rules
├── .gitignore                    # Project-specific Git ignore rules
├── .python-version               # Python version specification
├── .env.example                  # Example environment variables for backend
│
├── LICENSE                       # License specifying permissions and usage rights
└── README.md                     # Project documentation
```

<hr>

## License
- This project is licensed under the [MIT License](LICENSE). You are free to use and modify the code as needed.

<div align="left">
  
**[`^        Scroll to Top       ^`](#churnlabs--customer-churn-prediction)**

</div>
