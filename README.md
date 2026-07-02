<h3 align="center" id="top">ChurnLabs : Customer Churn Prediction System</h3>

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live-Demo-00C7B7?style=flat&logo=netlify&logoColor=white)](https://churnlabs.netlify.app)
[![API Docs](https://img.shields.io/badge/API-Docs-019486?style=flat&logo=fastapi&logoColor=white)](https://churnlabs.onrender.com/docs)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-Image-2496ED?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/u/themrityunjaypathak)
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
- [Overview](#overview)
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
- Telecom companies lose customers every month without knowing who is about to leave until it's too late.
- Identifying churners early allows businesses to intervene with the right offer before the customer cancels.
- This project predicts which customers are likely to churn, so retention teams can act early instead of reacting late.

<hr>

## Overview
- Built an end-to-end churn prediction system on 7,000+ customer records from PostgreSQL using Scikit-learn pipelines, ensuring reproducible training and preventing data leakage.
- Evaluated 7 classification models including a DummyClassifier baseline, selecting Logistic Regression based on recall and PR-AUC given class imbalance, with per-fold metrics tracked in MLflow.
- Optimized the decision threshold via precision-recall curve, targeting ≥90% recall on the churn class while accepting a precision drop as missing a churner outweighs a false retention offer.
- Deployed a Dockerized FastAPI backend on Render with a React frontend on Netlify, pulling the trained model from Hugging Face Hub as a remote artifact store for on-demand risk scoring.

<hr>

## Quick Start
- Choose the setup path that fits your situation :

**Path A : You have a PostgreSQL database configured**
```bash
git clone https://github.com/themrityunjaypathak/ChurnLabs.git
cd ChurnLabs

make install-dev     # Install dependencies and setup virtual environment

make ingest          # Fetch data from PostgreSQL
make preprocess      # Clean and transform the data
make train           # Train the model

make api-dev         # Start FastAPI backend → http://localhost:8000
make frontend-dev    # Start React frontend → http://localhost:5173
```

**Path B : You don't have a PostgreSQL database (use local dataset instead)**
```bash
git clone https://github.com/themrityunjaypathak/ChurnLabs.git
cd ChurnLabs

make install-dev     # Install dependencies and setup virtual environment
```
Then download the dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) and place it at :
```
data/raw/customer-churn-raw.csv
```
Then continue :
```bash
make preprocess      # Clean and transform the data
make train           # Train the model

make api-dev         # Start FastAPI backend → http://localhost:8000
make frontend-dev    # Start React frontend → http://localhost:5173
```

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
- Achieved 90% recall on the held-out test set, correctly flagging 335 out of 374 churners while missing only 39, with no overfitting between train and test set.
- Accepted a deliberate precision drop from 49% to 43% by tuning the decision threshold from 0.5 to 0.3632, as the cost of a false retention offer is lower than losing a churner.

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

<hr>

### 3. Run Data Ingestion
- This step extracts raw customer data from a PostgreSQL database and stores it locally for further processing.
- Run the ingestion pipeline :
```bash
make ingest
```

### What happens during ingestion?
- Connects to a PostgreSQL database using credentials stored in `.env`.
- Fetches customer churn data required for model training and evaluation.
- Stores raw dataset locally at `data/raw/customer-churn-raw.csv`.

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
3. Clean & Optimize the Dataset
- Typical preprocessing steps include :
    - Removing Invalid Records
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
- If present, load from local storage.
- If not present, fetch from Hugging Face.

### Why this design?
- Enables seamless development using local artifacts.
- Avoids committing large binary files to the repository.
- Ensures production systems can operate without local dependencies.
- Provides a robust fallback mechanism for reliable model loading.

<hr>

### 6. Start the FastAPI Backend
- The FastAPI server exposes endpoints for serving predictions, health checks, and model metadata.
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
> When deploying the backend on Render, make sure to configure the secrets in the Render dashboard.
>
> Navigate to : **Render Dashboard → Your Service → Environment → Environment Variables**
>
> Add the following environment variables :
>
> ```bash
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

### 7. Start the React Frontend
- The frontend provides an interactive UI for generating on-demand churn predictions.
```bash
make frontend-dev
```
- This command installs the Node.js dependencies and starts the React development server at :
```
http://localhost:5173
```
- The frontend communicates with the FastAPI backend to send requests and display predictions.

> [!IMPORTANT]
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
> ```
> VITE_API_URL=your_base_api_url
> ```
>
> This variable defines the base API URL that the React frontend will use for generating predictions.
>
> Without this variable, the frontend will still attempt to connect to the local API (`localhost:8000`).

Access the live application [here](https://churnlabs.netlify.app) or Click on the Image below.

<a href="https://churnlabs.netlify.app"><img title="React Frontend" src="https://github.com/user-attachments/assets/f5760807-0c32-4d2f-bcf8-e94423ec3e80"></a>

<hr>

### 8. Start Entire Application with Docker
- Instead of running services manually, you can start the entire application using Docker.
```bash
make compose-up-build
```
- Docker Compose will build and start all required services for the application using `docker-compose.yaml`.

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

### 9. Push Entire Application to Docker Hub
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
> <a href="https://hub.docker.com/r/themrityunjaypathak/churnlabs-api"><img title="Backend Docker Image" src="https://github.com/user-attachments/assets/bda95280-5eb1-4f66-a969-b5fe42932e71"></a>
>
> View the Frontend Docker Image [here](https://hub.docker.com/r/themrityunjaypathak/churnlabs-frontend) or Click on the Image below.
>
> <a href="https://hub.docker.com/r/themrityunjaypathak/churnlabs-frontend"><img title="Frontend Docker Image" src="https://github.com/user-attachments/assets/64cbbe66-e97f-4cb4-a245-cb4a67959f17"></a>

<hr>

### 10. Stop the Application
- This step stops and removes all running containers.
```bash
make compose-down
```

<hr>

## Config-Driven Design
- This project adopts a config-driven approach to manage data, model, training, and artifacts.
- Instead of hardcoding values inside the codebase, these settings are stored in YAML configuration files.
- These files are loaded during preprocessing, training, inference, and artifacts logging.
```
config/
├── data-config.yaml
├── model-config.yaml
├── training-config.yaml
├── huggingface-config.yaml
└── artifacts-config.yaml
```

<img title="Config Files" src="https://github.com/user-attachments/assets/745c635f-2f0f-473f-ae63-a9be08fe4fd0">

### Why Config-Driven design?

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

<img title="uv by Astral" src="https://github.com/user-attachments/assets/8427afdd-6642-49bb-bcb3-ae1b9b22be4e">

### Why use `uv` over `pip`?

### 1. Faster Dependency Installation
- `uv` is significantly faster than `pip` due to its optimized resolver and parallel package installation.
- This reduces setup time, especially for large projects with many dependencies.
```bash
uv sync
```
- In this project, uv sync reads from `uv.lock` and installs all dependencies in one step.

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
- A Makefile is a configuration file used by the `Make` build tool.
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
```bash
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

### Install `Make` on Windows via WSL

<details>
<summary>Click Here for More Details</summary>
<br>
	
- Windows does not include the `Make` utility by default.
- The easiest and most reliable way to use `Make` is through WSL.

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
```
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
```
GNU Make 4.x
Built for x86_64-pc-linux-gnu
```
- This confirms that `Make` is installed successfully.
- Remember, `Make` is available only inside the WSL terminal, not in Windows Command Prompt or PowerShell.

</details>

### Install `uv` in WSL

<details>
<summary>Click Here for More Details</summary>
<br>

- All Makefile commands are driven by `uv` under the hood.
- This means `uv` must be installed inside WSL first after WSL and `Make` are set up

### Step 1 : Open Your WSL (Ubuntu) Terminal
- Open the Start Menu
- Search for Ubuntu
- Launch the App

### Step 2 : Install `uv`
- Run the following command inside the WSL terminal :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- This downloads and installs `uv` to `~/.local/bin`.

### Step 3 : Update Your Shell PATH
- If `uv` isn't recognized after installation, reload your shell config :
```bash
source ~/.bashrc
```
- Or open a new WSL terminal window.

### Step 4 : Verify `uv` Installation
- Check that `uv` was installed correctly :
```bash
uv --version
```
- You should see output similar to : `uv 0.x.x`
- Once `uv` is installed and verified, all `make` commands will work as expected.

</details>

### Use `Make` in VS Code via WSL

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

### Step 4 : Open Project in WSL
- In VS Code, press `Ctrl + Shift + P`
- Type `WSL: Open Folder in WSL`
- Navigate to your project folder
- This ensures all terminal commands run inside WSL, not Windows

</details>

<hr>

## Experiment Tracking
- This project uses MLflow to track machine learning experiments, compare models, and log artifacts.
- MLflow ensures reproducibility by tracking parameters, metrics, and artifacts in a centralized dashboard.

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

<img title="MLflow UI" src="https://github.com/user-attachments/assets/0ba7f77b-c46d-4a14-817a-87a6645e7cf1">

### Types of Experiments Performed
- During model development, two types of experiments were performed and tracked using MLflow.

### 1. Model Comparison
- MLflow makes it easy to compare multiple models trained during experimentation.
- For this project, seven classification models were evaluated on the same stratified 5-fold splits, including :
	- Dummy Classifier 
    - Logistic Regression
    - K-Nearest Neighbors
    - Support Vector Classifier
    - Decision Tree
    - Random Forest
    - Gradient Boosting
- Metrics tracked per model :
    - Accuracy
    - Precision
    - Recall
    - F1-Score
    - ROC-AUC
    - PR-AUC
- This helps identify the best-performing model based on business requirements.

<img title="Model Comparison" src="https://github.com/user-attachments/assets/0740a01c-e806-426f-85ef-fbd904e6ffc5">

### 2. Threshold Optimization
- After selecting the best-performing model, another experiment is conducted to optimize the decision threshold.
- Instead of using the default threshold of 0.5, out-of-fold probabilities from cross-validation were used,
- To plot the precision-recall curve and identify the threshold that achieves ≥90% recall while maximizing precision.
- These experiments focused on :
    - Analyzing recall across different thresholds.
    - Selecting a threshold that meets business requirements.
    - Balancing precision-recall trade-offs.
- Optimal threshold selection allowed the model to achieve \~90% recall for the churn class.
- This approach allows the trade-off between the two thresholds to be compared directly in the MLflow UI.

<img title="Threshold Optimization" src="https://github.com/user-attachments/assets/cc8281f6-6d36-4f61-92a0-4b84907dfc5b">

### Logged Artifacts
- MLflow also stores experiment artifacts generated during training.
- Artifacts logged in this project include confusion matrix and classification reports.
- These artifacts help analyze model behavior and support model selection.

> [!NOTE]
> You can also reset MLflow experiments and remove stored runs for newer ones.
>
> To reset MLflow experiments, run this command from the project root directory :
> 
> ```bash
> make mlflow-clean
> ```
>
> Resetting MLflow means permanently deleting all experiments, runs, metrics, and artifacts stored locally.

<img title="Logged Artifacts" src="https://github.com/user-attachments/assets/245a8a8b-18a3-4c7c-aa51-c2ae25027127">

<hr>

## Model Training & Evaluation

### 1. Loading the Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Importing load_processed_data function from loaders module
from churnlabs.data.loaders import load_processed_data
churn_data = load_processed_data()
churn_data.head()
```
</details>

<hr>

### 2. Splitting the Data

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

### 3. Encoding Target Variable

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

### 4. Building Preprocessing Pipeline

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Transformation for Categorical Columns
cat_cols = X_train.select_dtypes(include='category').columns

cat_trf = Pipeline(steps=[
    ('ohe', OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore'))
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
# Combining Everything into ColumnTransformer
ctf = ColumnTransformer(transformers=[
    ('categorical', cat_trf, cat_cols),
    ('numerical', num_trf, num_cols)
], remainder='passthrough', n_jobs=-1)
```
</details>

<hr>

### 5. Training a Baseline Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

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
```python
# Stratified K-Fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```
```python
# Cross-Validation Setup
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision',
    'recall': 'recall',
    'f1_score': 'f1',
    'roc_auc': 'roc_auc',
    'pr_auc': 'average_precision'
}

cv = cross_validate(estimator=pipe, X=X_train, y=y_train, cv=skf, scoring=scoring, n_jobs=-1)
```
```python
# Cross-Validation Result
results = {metric.replace('test_', ''): [np.mean(scores), np.std(scores)] for metric, scores in cv.items() if metric.startswith('test')}
results_df = pd.DataFrame(results, index=['mean', 'std']).T
results_df
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

| | mean | std |
|:---:|:---:|:---:|
| accuracy | 0.7342 | 0.0 |
| precision	| 0.0000 | 0.0 |
| recall | 0.0000	| 0.0 |
| f1_score | 0.0000 | 0.0 |
| roc_auc | 0.5000 | 0.0 |
| pr_auc | 0.2657	| 0.0 |

### What does the `DummyClassifier` tell us?
- The `DummyClassifier` gives us a baseline to compare against real models.
- It predicts the majority class (`non-churn`) for every customer, ignoring all features.
```
# Class Distribution
churn
No     0.7342
Yes    0.2657
```
```
# Classification Metrics
accuracy    73%
precision   0
recall      0
f1_score    0
roc_auc     0.5
pr_auc      0.26
```
- Since the dataset contains ~73% non-churn customers, the model achieves 73% accuracy.
- However, it fails to identify any churners, resulting in zero precision, recall, and F1-Score.
- A model that never identifies a churner is useless, making recall and PR-AUC the only metrics that matter.
- ROC-AUC of 0.5 and PR-AUC of 0.26 confirm no predictive power, performing equivalent to random guessing.
- The `DummyClassifier` makes exactly the same prediction in every fold.
- So every fold produces identical metrics, and that's why standard deviation is equal to 0.
- This confirms our pipeline and cross-validation setup behave as expected.
- Now any real model must surpass this benchmark to be considered a good performer.
```
# Real Model Expectations
Achieve PR-AUC > 0.26
Achieve ROC-AUC > 0.5
Achieve Precision > 0
Achieve Recall > 0
Achieve F1-Score > 0
```
- If a trained model cannot outperform this baseline, it is not useful.
</details>

<hr>

### 6. Multi-Model Comparison

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Multi-Model Dictionary 
models = {
    'DC': DummyClassifier(strategy='most_frequent', random_state=42),
    'LR': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    'KNN': KNeighborsClassifier(n_jobs=-1),
    'SVC': SVC(class_weight='balanced', probability=True, random_state=42),
    'DT': DecisionTreeClassifier(class_weight='balanced', random_state=42),
    'RF': RandomForestClassifier(class_weight='balanced', random_state=42, n_jobs=-1),
    'GB': GradientBoostingClassifier(random_state=42)
}
```
```python
# Plotting Metric Comparision Graph
for model in results_df.columns:
    print()
    print(f'Model : {model}')
    print('-' * 40)
    print(f'Recall    : {results_df.loc["recall_mean", model]:.2f}')
    print(f'PR-AUC    : {results_df.loc["pr_auc_mean", model]:.2f}')
    print(f'ROC-AUC   : {results_df.loc["roc_auc_mean", model]:.2f}')
    print(f'F1-Score  : {results_df.loc["f1_score_mean", model]:.2f}')
    print(f'Precision : {results_df.loc["precision_mean", model]:.2f}')
    print(f'Accuracy  : {results_df.loc["accuracy_mean", model]:.2f}')
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Model : DC
----------------------------------------
Recall    : 0.00
PR-AUC    : 0.27
ROC-AUC   : 0.50
F1-Score  : 0.00
Precision : 0.00
Accuracy  : 0.73

Model : LR
----------------------------------------
Recall    : 0.80
PR-AUC    : 0.66
ROC-AUC   : 0.85
F1-Score  : 0.63
Precision : 0.52
Accuracy  : 0.75

Model : KNN
----------------------------------------
Recall    : 0.53
PR-AUC    : 0.52
ROC-AUC   : 0.78
F1-Score  : 0.55
Precision : 0.56
Accuracy  : 0.77

Model : SVC
----------------------------------------
Recall    : 0.79
PR-AUC    : 0.60
ROC-AUC   : 0.83
F1-Score  : 0.62
Precision : 0.52
Accuracy  : 0.75

Model : DT
----------------------------------------
Recall    : 0.49
PR-AUC    : 0.38
ROC-AUC   : 0.65
F1-Score  : 0.49
Precision : 0.50
Accuracy  : 0.73

Model : RF
----------------------------------------
Recall    : 0.47
PR-AUC    : 0.63
ROC-AUC   : 0.83
F1-Score  : 0.55
Precision : 0.64
Accuracy  : 0.79

Model : GB
----------------------------------------
Recall    : 0.51
PR-AUC    : 0.66
ROC-AUC   : 0.85
F1-Score  : 0.58
Precision : 0.66
Accuracy  : 0.80
```

<img title="Model Comparison" src="https://github.com/user-attachments/assets/dc5dcb22-c21b-4440-a5eb-9478f53a96c9">

</details>

<hr>

### 7. Selecting `LogisticRegression` as Final Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Creating LogisticRegression Model Object
lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
```
```python
# Final Pipeline with LogisticRegression
pipe = Pipeline(steps=[
        ('preprocessor', ctf),
        ('model', lr)
    ])
```
```python
# Cross-Validation Predict
y_pred_cv = cross_val_predict(estimator=pipe, X=X_train, y=y_train, cv=skf, method='predict', n_jobs=-1)
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

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

<img title="Confusion Matrix Plot" src="https://github.com/user-attachments/assets/d2d45a25-3ba1-4824-b481-3ec7bbdb03d2">

</details>

<hr>

### 8. Feature Importance 

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Fitting the Pipeline
pipe.fit(X_train, y_train)
```
```python
# Raw Column Names from ColumnTransformer (like 'numerical__totalcharges')
raw_features = pipe.named_steps['preprocessor'].get_feature_names_out()
```
```python
# Clean Column Names (splitting based on '__' and extracting 2nd element)
features = [feature.split('__')[1] for feature in raw_features]
```
```python
# Coefficients from LogisticRegression
coefficients = pipe.named_steps['model'].coef_[0]
```
```python
# Feature Importance DataFrame
importance_df = pd.DataFrame({'feature': features, 'importance': coefficients}).sort_values(by='importance', ascending=False)
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

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

<img title="Feature Importance Plot" src="https://github.com/user-attachments/assets/655319e5-6844-470e-8708-f95ff33795ac">

### Feature Importance Interpretation
Values represent impact on log-odds of churn.
- 🟢 Positive coefficients → Increase churn risk
- 🔴 Negative coefficients → Decrease churn risk

</details>

<hr>

### 9. Decision Threshold Tuning

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Cross-Validation Predict
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
```
```python
# Evaluate Recall across Thresholds and Choose Best Threshold
valid = pr_results[pr_results["recall"] >= recall_target]

if not valid.empty:
    best_row = valid.loc[valid["precision"].idxmax()]
    best_threshold = best_row["threshold"]
else:
    best_threshold = 0.5
    print("Warning: No threshold achieved target recall of 0.90. Falling back to 0.5.")

print(f"Best Threshold: {best_threshold:.4f}")
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>
	
```
Best Threshold: 0.3632
```
</details>

<hr>

### 10. Performance Evaluation with Tuned Threshold

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Best Threshold
y_pred_best = (y_proba_cv >= best_threshold).astype(int)
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```python
# Classification Report
print(classification_report(y_train, y_pred_best, target_names=['No', 'Yes']))
```
```
			  precision    recall  f1-score   support

          No       0.95      0.61      0.74      4130
         Yes       0.45      0.90      0.60      1495

    accuracy                           0.69      5625
   macro avg       0.70      0.76      0.67      5625
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

<img title="Confusion Matrix Plot" src="https://github.com/user-attachments/assets/7aad908a-327d-4f35-bb12-e2e856a61878">

</details>

<hr>

### 11. Final Model Evaluation on Test Set

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Fitting Pipeline on Full Training Data
pipe.fit(X_train, y_train)
```
```python
# Test Set Probability used for both Default and Tuned Threshold
y_test_proba = pipe.predict_proba(X_test)[:, 1]
```
</details>

### Default Threshold

<details>
<summary>Click Here to view Analysis</summary>
<br>

```python
# Default Threshold
y_test_pred_default = (y_test_proba >= 0.5).astype(int)
```
```python
# Classification Report on Default Threshold
print(classification_report(y_test, y_test_pred_default, target_names=['No', 'Yes']))
```
```
              precision    recall  f1-score   support

          No       0.90      0.70      0.79      1033
         Yes       0.49      0.80      0.61       374

    accuracy                           0.73      1407
   macro avg       0.70      0.75      0.70      1407
weighted avg       0.79      0.73      0.74      1407
```
```python
# Plotting Confusion Matrix on Default Threshold
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred_default, display_labels=['No', 'Yes'], cmap='crest', ax=ax[0])
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred_default, display_labels=['No', 'Yes'], cmap='crest', normalize='all', ax=ax[1])
ax[0].set_title('Confusion Matrix at Default Threshold (Counts)')
ax[1].set_title('Confusion Matrix at Default Threshold (Normalized)')
ax[0].grid(visible=False)
ax[1].grid(visible=False)
plt.tight_layout()
plt.show()
```

<img title="Confusion Matrix Plot on Default Threshold" src="https://github.com/user-attachments/assets/cae5a413-d0e9-455c-aa10-b9731c21e90a">

</details>

### Tuned Threshold

<details>
<summary>Click Here to view Analysis</summary>
<br>

```python
# Tuned Threshold
y_test_pred_tuned = (y_test_proba >= best_threshold).astype(int)
```
```python
# Classification Report on Tuned Threshold
print(classification_report(y_test, y_test_pred_tuned, target_names=['No', 'Yes']))
```
```
              precision    recall  f1-score   support

          No       0.94      0.58      0.71      1033
         Yes       0.43      0.90      0.58       374

    accuracy                           0.66      1407
   macro avg       0.69      0.74      0.65      1407
weighted avg       0.80      0.66      0.68      1407
```
```python
# Plotting Confusion Matrix on Tuned Threshold
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred_tuned, display_labels=['No', 'Yes'], cmap='crest', ax=ax[0])
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred_tuned, display_labels=['No', 'Yes'], cmap='crest', normalize='all', ax=ax[1])
ax[0].set_title('Confusion Matrix at Tuned Threshold (Counts)')
ax[1].set_title('Confusion Matrix at Tuned Threshold (Normalized)')
ax[0].grid(visible=False)
ax[1].grid(visible=False)
plt.tight_layout()
plt.show()
```

<img title="Confusion Matrix Plot on Tuned Threshold" src="https://github.com/user-attachments/assets/730a3b6c-fa0b-4971-a48c-abe82e362c6f">

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
│   ├── package-lock.json         # Dependency lock file
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
│
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
│   │
│   └── churnlabs/
│       │
│       ├── core/                 # Core utility module
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── logger.py
│       │   └── settings.py
│       │
│       ├── data/                 # Data loading and preprocessing module
│       │   ├── __init__.py
│       │   ├── ingestion.py
│       │   ├── loaders.py
│       │   ├── preprocessor.py
│       │   └── export.py
│       │
│       ├── features/             # Feature engineering module
│       │   ├── __init__.py
│       │   └── split.py
│       │
│       ├── models/               # Model training and evaluation module
│       │   ├── __init__.py
│       │   ├── artifact.py
│       │   ├── builder.py
│       │   ├── encoder.py
│       │   ├── evaluation.py
│       │   ├── pipeline.py
│       │   ├── transformer.py
│       │   ├── loader.py
│       │   └── uploader.py
│       │
│       └── __init__.py
│
├── .dockerignore                 # Backend Dockerignore rules
├── .env.example                  # Example environment variables for backend
├── .gitignore                    # Project-specific Git ignore rules
├── .python-version               # Python version specification
├── LICENSE                       # License specifying permissions and usage rights
├── Makefile                      # Project commands (MLflow, FastAPI, React, Docker, etc.)
├── README.md                     # Project documentation
├── docker-compose.yaml           # Docker orchestration for backend and frontend
├── mlflow.db                     # MLflow experiment tracking database (ignored by Git)
├── netlify.toml                  # Netlify deployment configuration
├── pyproject.toml                # Python project configuration
└── uv.lock                       # Dependency lock file
```

<hr>

## License
- This project is licensed under the [MIT License](LICENSE). You are free to use and modify the code as needed.

<div align="left">
  
**[`^        Scroll to Top       ^`](#top)**

</div>
