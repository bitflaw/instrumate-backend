This is InstruMate Africa, a project that leverages ML and avatars to enable effective learning for differently abled learners
## Overview

InstruMate Africa is an innovative platform that uses machine learning and avatar technology to create accessible and engaging educational experiences for differently abled learners across Africa.

## What It Does

- Delivers personalized learning paths powered by AI
- Uses interactive avatars to enhance engagement
- Prioritizes accessibility for all users
- Supports multiple languages
- Provides analytics dashboards for educators

## Main Technologies Used

- Python
- TensorFlow
- PyTorch
- React

## Build Instructions

To set up and build the project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/FRANCISMUNGANGU/InstruMate-Africa.git
    cd InstruMate-Africa
    ```

2. **Set up the Python backend:**
    - Create and activate a virtual environment:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    
    - Remove Bulky dependencies (if any):
      ```bash
      pip uninstall -r to_delete.txt -y
      ```
    
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

3. **Set up the React frontend:**
    - Navigate to the frontend directory (replace `frontend` with the actual folder name if different):
      ```bash
      cd frontend
      ```
    - Install dependencies:
      ```bash
      npm install
      ```

4. **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```

5. **Run the frontend development server:**
    ```bash
    npm start
    ```

6. **Access the application:**
    - Open your browser and go to `http://localhost:3000` for the frontend.
    - The backend API will be available at `http://localhost:8000`.

> **Note:** Make sure you have Python 3.8+ and Node.js 14+ installed.

- FastAPI

> **Note:** This project is currently private and not publicly accessible.
