# UlinziMind AI Sentinel: Real-Time Predictive Intelligence

## Overview

UlinziMind AI Sentinel is a proof-of-concept full-stack application designed to demonstrate the power of AI fusion for national security and public safety. The platform integrates data from disparate sources—simulated satellite imagery and social media streams—to generate unified, predictive security alerts. A core focus of the architecture is the **Ethical Design** principle, including a module to appropriately flag and manage peaceful civic protests.

The system is split into a robust Python/FastAPI backend hosting the AI core, and a responsive React/Vite frontend for real-time visualization and user authentication.

## Features

* **Multi-Modal AI Fusion:** Combines insights from Computer Vision (CV) and Natural Language Processing (NLP) using a simulated Graph Neural Network (GNN) engine to produce a unified `risk_score`.
* **Geospatial Intelligence:** Integrates a YOLOv8-based Computer Vision pipeline to detect and quantify physical assemblies and object movements in real-time (using simulated satellite imagery).
* **Social Intelligence:** Utilizes a BERT-based Hugging Face sentiment analysis model to analyze simulated social media streams for digital unrest, hate speech, and misinformation.
* **Ethical Design (Civic Peace Module):** Includes logic to identify peaceful civic protests (high object count, low risk score) and recommends non-violent monitoring and de-escalation actions, capping the reported risk for non-violent events.
* **Real-Time Dashboard:** A modern React/Leaflet frontend provides an interactive map visualization of alerts, real-time filtering, and KPI summaries.
* **Secure Authentication:** Uses Firebase Authentication for user sign-up and sign-in.

## Tech Stack

| Component | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | `Python`, `FastAPI` | Core API for processing and serving alerts. |
| **AI/ML** | `YOLOv8`, `HuggingFace Transformers` | Models powering the Computer Vision and NLP Sentinels. |
| **Data Fusion** | `UlinziMindEngine` (GNN Simulation) | Fuses multi-modal data into a single predictive `risk_score`. |
| **Frontend** | `React 19`, `Vite` | Modern single-page application framework. |
| **Authentication**| `Firebase Auth` | Handles user identity management. |
| **Mapping** | `Leaflet`, `React-Leaflet` | Interactive map visualization for geospatial data. |
| **Networking** | `Axios` | Used for client-side API communication with FastAPI. |

## Setup & Installation

The project requires two independent setups for the backend and frontend.

### Prerequisites

* **Python 3.x** (with `pip` and `venv`)
* **Node.js 18+** (with `npm`)
* *(Optional but recommended)* CUDA/GPU setup if attempting to run the full `ultralytics` and `transformers` dependencies without falling back to stub logic.

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd Backend_work
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    *(Note: If the necessary AI dependencies are not installed or configured correctly, the `ai_core.py` will use stub classes, and the API will serve simulated alert data, allowing the frontend to load.)*
    ```bash
    # Assuming all necessary Python packages are listed in a requirements file.
    # pip install -r requirements.txt 
    
    # Or manually for the core framework:
    # pip install fastapi uvicorn 
    # pip install numpy ultralytics transformers  # For full AI functionality
    ```

4.  **Run the FastAPI server:**
    The API will run at `http://127.0.0.1:8000`.
    ```bash
    uvicorn main:app --reload
    ```

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd Frontend_work/ulinzi_front
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Firebase Configuration (Important)**
    The project uses Firebase Authentication. The default configuration is included in `src/context/AuthContext.jsx`.
    
    | Key | Value |
    | :--- | :--- |
    | `apiKey` | `AIzaSyDU_xPuE1EkpGGvFae2nH9_khctiV5dUJY` |
    | `authDomain` | `ulinzimind.firebaseapp.com` |
    | `projectId` | `ulinzimind` |
    
    **For testing/production, you must replace these placeholder values with your own secure Firebase configuration.**

4.  **Run the React development server:**
    The application will typically run at `http://localhost:5173`.
    ```bash
    npm run dev
    ```

## Usage & Demo

1.  Ensure both the **FastAPI Backend** and the **React Frontend** are running concurrently in separate terminals.
2.  Open your browser to the frontend URL (e.g., `http://localhost:5173`).
3.  Use the **Register** link to create a new user account via Firebase.
4.  **Log in** with the credentials. The provided placeholder credentials (referenced in `src/components/Login.jsx`) for demo use are:
    * **Email**: `user@example.com`
    * **Password**: `password`
5.  Upon logging in, the **Dashboard** will load and automatically begin fetching real-time alerts from the backend API at `http://127.0.0.1:8000/api/v1/alerts` every 5 seconds. Alerts will be displayed on the map and in the paginated table.
