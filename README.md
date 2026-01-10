# 🎬 End-to-End Movie Recommendation System

An end-to-end **content-based movie recommendation system** built using **NLP, TF-IDF, and Cosine Similarity**, integrated with the **TMDB API**, and deployed with a **FastAPI backend** and an **interactive Streamlit frontend**.

This project demonstrates the complete lifecycle of a real-world ML system — from data preprocessing and model training to API-based inference and user-facing deployment.

---

## 🚀 Features

- 🔍 **Movie Search & Autocomplete** using TMDB API  
- 🤖 **Content-Based Recommendations** using TF-IDF + Cosine Similarity  
- 🎭 **Genre-Based Recommendations** via TMDB discovery  
- 🧠 **NLP Preprocessing** on movie metadata  
- ⚡ **FastAPI Backend** for scalable ML inference  
- 🖥️ **Streamlit Frontend** for interactive exploration  
- 🌐 **Deployed Architecture** (Backend + Frontend separated)

---

## 🧱 Tech Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- Pandas, NumPy
- TMDB API

### Machine Learning
- NLP preprocessing
- TF-IDF Vectorization
- Cosine Similarity

### Frontend
- Streamlit

### Deployment
- Backend: Render
- Frontend: Streamlit Cloud / HuggingFace Spaces



---

## 🔄 How It Works

1. Movie metadata is preprocessed using NLP techniques.
2. A TF-IDF matrix is built from textual features.
3. Cosine similarity is used to compute movie similarity.
4. FastAPI serves recommendations via REST APIs.
5. Streamlit consumes these APIs to provide an interactive UI.

---

## ▶️ Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

