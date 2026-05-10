# AI Text Summarizer

A full-stack application that leverages advanced AI models to generate concise summaries of long texts and PDF documents. Built with React (Vite) on the frontend and FastAPI on the backend.

## 🚀 Features

- **Text Summarization**: Paste any long article or text to get an instant summary.
- **PDF Summarization**: Upload PDF documents, and the app will extract and summarize the contents automatically.
- **Local AI Execution**: Uses the HuggingFace `sshleifer/distilbart-cnn-12-6` model via Transformers for fast and secure local processing.
- **Premium UI**: A sleek, fully responsive, glassmorphism-inspired dark mode interface.

## 🛠️ Technology Stack

- **Frontend**: React, Vite, Vanilla CSS
- **Backend**: FastAPI, Uvicorn, PyTorch, Transformers, PyPDF2
- **AI Model**: DistilBART CNN (HuggingFace)

## 💻 Local Development Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd "AI Text Summarizer"
```

### 2. Backend Setup
The backend runs on FastAPI and requires Python.
```bash
cd backend
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload
```
The API will run at `http://localhost:8000`.

### 3. Frontend Setup
The frontend is built with React and Vite. Open a new terminal window.
```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
The web app will run at `http://localhost:5173`.

## 🌐 Deployment Guidelines

- **Backend (Render)**: Set the root directory to `backend`, build command to `pip install -r requirements.txt`, and start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Frontend (Vercel)**: Set the root directory to `frontend`, build command to `npm run build`. Add an environment variable `VITE_API_URL` pointing to your deployed Render backend URL.

## 📝 License
This project is open-source and available under the MIT License.
